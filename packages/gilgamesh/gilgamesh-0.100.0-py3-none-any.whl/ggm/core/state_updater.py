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
import time
import asyncio
from zmq.utils.strtypes import asbytes

from ..lib.kernel import GK
from ..lib.kontext import Kontext

from datetime import datetime as dt
from pprint import pprint

class GStateUpdater(GK):
    def __init__(self, *args, **kwargs):
        self.loop = kwargs['loop']
        self.context = kwargs['context']
        self.name = kwargs['name']

        self.FRO = "ipc:///tmp/frontend"
        self.fro = self.context.socket(zmq.DEALER)
        self.fro.connect(self.FRO)

        GK.__init__(self, *args, **kwargs)

        self.loop.create_task(self.update_state())

    async def update_state(self):
        """
        TODO
        cache?
        """
        while True:
            rand_sleep = round(random.uniform(0.5,1.5), 2)
            await asyncio.sleep(60*rand_sleep)
            #await asyncio.sleep(3)
            start_time = time.time()

            iq = ['series', 'inventory', self.dev_id, 'all']
            await self.fro.dsend(iq)
            route, state = await self.fro.drecv()
            #pprint(state)
            # FIXME workaround for unknown errors
            state.pop("Error", None)
            state.pop("Reason", None)

            up_query = ['json', 'nupsert', 'device_state_db', self.dev_id, state]
            await self.fro.dsend(up_query)
            route, reply = await self.fro.drecv()
            #pprint(reply)

            # update 'seen' and dev_id
            tmst = self.get_iso_timestamp()
            up_request = ['json', 'nupsert', 'device_state_db', self.dev_id, {'seen': tmst, 'dev_id': self.dev_id}]
            await self.fro.dsend(up_request)
            route, reply = await self.fro.drecv()
            #pprint(reply)

            # update store
            store = {'store': {}}
            dq = ['json', 'get', 'device_state_db', 'all', 'head']
            await self.fro.dsend(dq)
            route, devs = await self.fro.drecv()
            #pprint(devs)
            # FIXME workaround for unknown errors
            devs.pop("Error", None)
            devs.pop("Reason", None)

            for dev in devs['device_state_db'].keys():
                if dev == self.dev_id:
                    continue
                iq = ['series', 'inventory', dev, 'all']
                await self.fro.dsend(iq)
                route, dev_inv = await self.fro.drecv()
                #print(dev, dev_inv)
                store['store'][dev] = dev_inv.pop('inventory')

            if store['store']:
                #self.glog.debug(f'Updating Store.')
                up_query = ['json', 'nupsert', 'device_state_db', self.dev_id, store]
                await self.fro.dsend(up_query)
                route, response = await self.fro.drecv()
                #print(response)
                del store['store']

            stop_time = time.time()
            self.glog.debug(f'State Update took: {round((stop_time-start_time), 3)} s')
            
def state_updater_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop
    
    updater = GStateUpdater(**kcfg)
    updater.start()
