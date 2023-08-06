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
import asyncio
from zmq.utils.strtypes import asbytes

class GHeartt(object):
    """
    heartbeater/handle_pong -> coroutines for hearbeater
    heart -> zmq thread device
    TODO write doc
    """
    def __init__(self, *args, **kwargs):

        self.HEART  = "ipc:///tmp/heart"
        self.BEAT   = "ipc:///tmp/beat"

        self.hearts = set()
        self.responses = set()
        self.period = 15 # *2 ??? # FIXME strange behaviour?
        self.lifetime = 0
        self.tic = self.loop.time()

    async def start_heart(self):
        """
        heart coroutine
        """
        ping = self.context.socket(zmq.SUB)
        ping.subscribe(b"")
        ping.connect(self.HEART)
        pong = self.context.socket(zmq.PUB)
        pong.connect(self.BEAT)
        while True:
            msg = await ping.recv_multipart()
            msg.insert(0, asbytes(self.name))
            pong.send_multipart(msg)

    async def handle_pong(self):
        """
        if heart is beating
        """
        pong = self.context.socket(zmq.SUB)
        pong.subscribe(b"")
        pong.bind(self.BEAT)
        while True:
            msg = await pong.recv_multipart()
            if float(msg[1]) == self.lifetime:
                self.responses.add(msg[0].decode())
            else:
                self.glog.error("{0} Bad Heartbeat from {1}: {2}".format(self.lifetime, msg[0], msg[1]))

    async def heartbeater(self):
        """
        beat the devil out of it
        """
        ping = self.context.socket(zmq.PUB)
        ping.bind(self.HEART)
        while True:
            await asyncio.sleep(self.period)

            toc = self.loop.time()
            self.lifetime += toc-self.tic
            self.tic = toc

            goodhearts = self.hearts.intersection(self.responses)
            heartfailures = self.hearts.difference(goodhearts)
            newhearts = self.responses.difference(goodhearts)
            #print(newhearts, goodhearts, heartfailures)
            #list(map(...)) needed, or map will not get *executed* as expected
            list(map(self.handle_new_heart, newhearts))
            list(map(self.handle_heart_failure, heartfailures))
            self.responses = set()

            #print("%i beating hearts: %s"%(len(self.hearts),self.hearts))
            ping.send_string(str(self.lifetime))

    def handle_new_heart(self, heart):
        self.hearts.add(heart)

    def handle_heart_failure(self, heart):
        """
        restarts stopped kernels
        """
        self.hearts.remove(heart)
        self.glog.warning(f'(Heart Failure) {self.period}s of inactivity from {heart}')

        for n, kernel in enumerate(self.kernel_map):
            if kernel['name'] == heart:
                self.kernel_map[n]['proc'].terminate()
                self.init_kernel(self.kernel_map[n], n)
