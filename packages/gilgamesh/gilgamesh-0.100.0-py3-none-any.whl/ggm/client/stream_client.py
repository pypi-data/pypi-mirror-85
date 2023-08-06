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

import sys
import zlib
import json
import pickle
import asyncio
import zmq.auth
import time
import socket
from .auth import AuthClient

from datetime import datetime as dt

from pprint import pprint

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

class GStreamClient(AuthClient):
    def __init__(self, ggm_host='local',*args, **kwargs):
        """GILGAMESH™
        
        class GGM(ggm_host='local')
        
        ggm_host: sting found as key in config.json
        """
        self.version = '0.9'
        super().__init__(ggm_host, *args, **kwargs)
        
        self.client = self.get_client()

        self.poller = zmq.Poller()
        self.poller.register(self.client, zmq.POLLIN)

        assert self.check_conn()
        
        self.client.psend(['info'])
        reply = self.client.precv()
        self.remote_dev_id = reply['dev_id']

        self.stream = self.ctx.socket(zmq.SUB)
        self.stream.connect(f'tcp://{self.host_ip}:6003')
        self.poller.register(self.stream, zmq.POLLIN)

    def stream_sub(self, name, dev_id=None):
        dev_id = dev_id or self.remote_dev_id
        sub = f'{dev_id} {name}'
        self.stream.subscribe(sub.encode())
        return True

    def stream_unsub(self, name, dev_id=None):
        dev_id = dev_id or self.remote_dev_id
        sub = f'{dev_id} {name}'
        self.stream.unsubscribe(sub.encode())
        return True

    def get_latest(self):
        socks = dict(self.poller.poll(100))
        if socks.get(self.stream) == zmq.POLLIN:
            topic, payload = self.stream.recv_multipart()
            #return [measurement, json.loads(payload)]
            d = json.loads(payload.decode())
            return pd.DataFrame(data={k: v for k,v in d['fields'].items()}, index=pd.Series(np.datetime64(d['time'])))
        else:
            return 'no message :('

    def show_streams(self):
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()
        return [d for d in reply['device_state_db'][self.remote_dev_id]['inventory'].keys()]
    
    def check_conn(self):        
        self.client.psend(['greetings'])
        while True:
            socks = dict(self.poller.poll(1000))
            if socks.get(self.client) == zmq.POLLIN:
                ret = self.client.precv()
                if ret == ['earthlings']:
                    print('Connecting to gilgamesh successful!')
                    return True
                elif not ret == ['earthlings']:
                    print(f'failed greeting(!) got: {ret}\nretrying...')
                    self.client.psend(['greetings'])
                    continue
            elif not socks.get(self.client):
                self.terminate()
                print(f'Failed connecting to server please check settings!\n')
                return False

    def terminate(self):
        self.client.set(zmq.LINGER, 0)
        self.client.close()
        self.ctx.term()
        print(f'Terminated gilgamesh Client')
