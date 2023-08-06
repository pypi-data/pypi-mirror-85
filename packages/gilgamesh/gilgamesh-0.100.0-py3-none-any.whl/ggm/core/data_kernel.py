"""
GILGAMESH
Copyright (C) 2019  Contributors as noted in the AUTHORS file

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import zmq
import random
import json
import time
import asyncio
from zmq.utils.strtypes import asbytes

from ..lib.kernel import GK
from ..lib.kontext import Kontext

from datetime import datetime as dt
from datetime import timedelta as td
from pprint import pprint
from collections import defaultdict

class GData(GK):
    def __init__(self, *args, **kwargs):
        self.loop = kwargs['loop']
        self.context = kwargs['context']
        self.name = kwargs['name']

        self.BUFFER_MAX_AGE = td(seconds=kwargs['buffer_max_age'])
        self.BUFFER_MAX_SIZE = kwargs['buffer_max_size']
        self.VACUUM_INTERVAL = kwargs['vacuum_interval']
        self.buffer_map = defaultdict(dict)

        self.DIN = 'ipc:///tmp/data_in'
        self.PUB = f'tcp://0.0.0.0:{kwargs["port"]}'

        self.FRO = "ipc:///tmp/frontend"
        self.fro = self.context.socket(zmq.DEALER)
        self.fro.connect(self.FRO)

        self.DOUT = 'ipc:///tmp/data_out'
        self.outbound = self.context.socket(zmq.PUSH)
        self.outbound.bind(self.DOUT)

        GK.__init__(self, *args, **kwargs)

        self.loop.create_task(self.relay())
        self.loop.create_task(self.vacuum())

    async def relay(self):
        """doc
        """
        inbound = self.context.socket(zmq.PULL)
        inbound.bind(self.DIN)

        pub = self.context.socket(zmq.PUB)
        pub.bind(self.PUB)
        # beware of slow subscribers!
        #pub.setsockopt(zmq.CONFLATE, 1)

        while True:
            msg = await inbound.precv()
            try:
                db, tb = (msg[0], msg[1])
            except:
                self.glog.error(f'Malicious data received. Check app sanity!')
            #self.glog.debug(f'Got data: {msg}')

            # check message integrity
            if not isinstance(msg[-1], list):
                # FIXME should be illegal (filter elsewhere?)
                if isinstance(msg[-1], dict):
                    self.glog.error(f'data dict received for: {db} - {tb}')
                    self.glog.error(f'dict: {msg[-1]}')
                    msg[-1] = [msg[-1]]
                else:
                    self.glog.error(f'big wtf: {db} - {tb}')
                    del db
                    del tb
                    del msg
                    continue
            elif len(msg[-1]) == 0:
                self.glog.info(f'empty data received for: {db} - {tb}')
                continue
            else:
                pass

            # add 'missing keys'
            if not 'tags' in msg[-1][0]:
                msg[-1][0]['tags'] = {}
            if not 'fields' in msg[-1][0]:
                msg[-1][0]['fields'] = {}

            # single points get published
            # data blocks > buffer size get redirected to database immediately
            if len(msg[-1]) == 1:
                # multipart is not possible with conflate!
                pub.send_multipart([f'{msg[0]} {msg[1]}'.encode(), json.dumps(msg[-1][0]).encode()])
            elif len(msg[-1]) >= self.BUFFER_MAX_SIZE:
                await self.outbound.psnd(msg)
                continue
            else:
                pass

            # create buffer for new data
            if not db in self.buffer_map:
                self.buffer_map[db] = {}
            if not tb in self.buffer_map[db]:
                self.buffer_map[db][tb] = {}

            # new data needs a data map created
            # if data is empty a new era begins
            # else (if data exists) add missing fields and tags
            if not 'data' in self.buffer_map[db][tb]:
                self.buffer_map[db][tb]['data'] = []
                self.buffer_map[db][tb]['age'] = dt.utcnow()
            elif not len(self.buffer_map[db][tb]['data']):
                self.buffer_map[db][tb]['age'] = dt.utcnow()
            else:
                for k in self.buffer_map[db][tb]['data'][0]['fields'].keys():
                    for i, d in enumerate(msg[-1]):
                        if k not in msg[-1][i]['fields']:
                            msg[-1][i]['fields'][k] = None
                for k in self.buffer_map[db][tb]['data'][0]['tags'].keys():
                    for i, d in enumerate(msg[-1]):
                        if k not in msg[-1][i]['tags']:
                            msg[-1][i]['tags'][k] = None

            # change and save tags only on change
            if not 'tags' in self.buffer_map[db][tb]:
                self.buffer_map[db][tb]['tags'] = msg[-1][-1]['tags']
            elif self.buffer_map[db][tb]['tags'] == msg[-1][-1]['tags']:
                msg[-1][-1]['tags'] = dict.fromkeys(msg[-1][-1]['tags'], None)
            else:
                self.buffer_map[db][tb]['tags'] = msg[-1][-1]['tags']

            #if len(self.buffer_map[db][tb]['data']) >= self.BUFFER_MAX_SIZE:
            #    await self.outbound.psnd([ db, tb, self.buffer_map[db][tb]['data']])
            #    self.buffer_map[db][tb]['data'] = msg[-1]
            #    continue
            #else:
            self.buffer_map[db][tb]['data'].extend(msg[-1])

    async def vacuum(self):
        """doc
        empty buffer map periodically
        """
        while True:
            await asyncio.sleep(self.VACUUM_INTERVAL)
            for db in self.buffer_map.keys():
                for tb in self.buffer_map[db].keys():
                    if ( ((dt.utcnow() - self.buffer_map[db][tb]['age']) > self.BUFFER_MAX_AGE
                            or len(self.buffer_map[db][tb]['data']) >= self.BUFFER_MAX_SIZE)
                            and len(self.buffer_map[db][tb]['data']) > 0 ):
                        await self.outbound.psnd([db, tb, self.buffer_map[db][tb]['data']])
                        self.buffer_map[db][tb]['data'] = []
                        self.buffer_map[db][tb]['age'] = dt.utcnow()
                    else:
                        pass


def data_kernel_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop
    
    data = GData(**kcfg)
    data.start()
