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
import json
import asyncio
from ..lib.kernel import GK
from ..lib.aiomqtthelper import AioMqttHelper
from ..lib.kontext import Kontext

import paho.mqtt.client as mqtt
import socket

from datetime import datetime as dt  # this
from datetime import timedelta as td # is
from datetime import timezone as tz  # madness

class GMqttBridge(GK, AioMqttHelper):
    def __init__(self, *args, **kwargs):
        GK.__init__(self, *args, **kwargs)

    def on_connect(self, client, userdata, flags, rc):
        print("Connecting")
    
    def on_message(self, client, userdata, message):
        #if not self.got_message:
        #    self.glog.debug("Got unexpected message: {}".format(msg.decode()))
        #else:
        #    self.got_message.set_result(json.loads(message.payload.decode()))
        self.got_message.set_result(message)

    def on_disconnect(self, client, userdata, rc):
        self.disconnected.set_result(rc)

    async def paho_loop(self):
        with open(f'/etc/gilgamesh/mqtt.secret', 'r') as raw:
            cfg = json.load(raw)

        self.disconnected = self.loop.create_future()
        self.got_message = None

        self.client = mqtt.Client()
        self.client.username_pw_set(cfg['username'], cfg['password'])
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        aioh = AioMqttHelper(self.loop, self.client)

        # fixme -> get all from config
        self.client.connect(cfg['hostname'], 1883, 60)
        self.client.socket().setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)
        self.client.subscribe(f'gilgamesh/data_in/#')

        del cfg

        while True:
            #await asyncio.sleep(1)
            self.got_message = self.loop.create_future()
            msg = await self.got_message
            self.got_message = None

            try:
                topic = msg.topic.split('/')
                topic.pop(0)
                topic.pop(0)
                dev_id = topic.pop(0)
                measurement = topic.pop(0)
                raw = msg.payload.decode()
                payload = json.loads(raw)
            except Exception as e:
                self.glog.error(f'bad mqtt message {dev_id}/{measurement} {raw}: {e}')
                continue

            fields, tags, time = [None]*3
            if 'fields' in payload:
                fields = payload['fields']
            if 'tags' in payload:
                tags = payload['tags']
            if 'time' in payload:
                time = payload['time']

            await self.send_data(dev_id, measurement, fields, tags, time)

def mqtt_bridge_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop

    bri = GMqttBridge(**kcfg)
    loop.create_task(bri.paho_loop())
    bri.start()
