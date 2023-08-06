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

import os
import zmq
import asyncio
from zmq.asyncio import Poller
from zmq.utils.strtypes import asbytes

from ..lib.kernel import GK
from ..lib.kontext import Kontext
from ..lib.auth import GAuthServer

class GIronBase(GAuthServer, GK):
    def __init__(self, *args, **kwargs):
        GK.__init__(self, *args, **kwargs)
        GAuthServer.__init__(self, *args, **kwargs)

        self.fro = self.context.socket(zmq.DEALER)
        self.fro.setsockopt(zmq.IDENTITY, asbytes(self.name))
        self.fro.connect("ipc:///tmp/frontend")

        # Initialize poll set
        self.poller = Poller()

        self.poller.register(self.fro, zmq.POLLIN)
        self.poller.register(self.server, zmq.POLLIN)

    async def recv_data(self):
        while True:
            socks = dict(await self.poller.poll())

            if socks.get(self.server) == zmq.POLLIN:
                route, message = await self.server.drecv(raw=True)
                #print(f'coming in: {message}')
                await self.fro.dsend(message, route, raw=True)

            if socks.get(self.fro) == zmq.POLLIN:
                route, message = await self.fro.drecv(raw=True)
                #print(f'coming out: {message}')
                await self.server.dsend(message, route, raw=True)


def ironbase_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop

    irn = GIronBase(**kcfg)
    loop.create_task(irn.recv_data())
    irn.start()
