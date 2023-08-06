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
import zmq
import asyncio

from .logging import GLog
from .heart import GHeartt
from .data import GData
from pprint import pprint

from time import sleep

class GK(GData, GHeartt, GLog):
    """
    gilgamesh kernel
    composes logger, heart, and data classes
    adds control coroutine
    """
    def __init__(self, *args, **kwargs):
        self.loop = kwargs['loop']
        self.context = kwargs['context']
        self.dev_id = kwargs['device_id']
        self.name = kwargs['name']
        self.version = kwargs['version']
        # Y U NO WORK???
        #super().__init__()
        GData.__init__(self, *args, **kwargs)
        GHeartt.__init__(self, *args, **kwargs)
        GLog.__init__(self, *args, **kwargs)

        sleep(2)

    async def control(self):
        """
        TODO:
        set log lvl
        stop self?
        extensions via superclass?
        """
        sname = "ipc:///tmp/ctrl_{0}".format(self.name)
        rep = self.context.socket(zmq.REP)
        rep.connect(sname)
        while True:
            raw = await rep.precv()
            await rep.psnd(raw)

    def start(self, *args, **kwargs):
        self.loop.create_task(self.start_heart())
        self.loop.run_forever()

    def stop(self, *args, **kwargs):
        """
        TODO
        do a nice termination...
        """
        self.glog.info('Stopping Kernel {0} gracefully.'.format(self.name))
        self.loop.stop()
        sys.exit(0)
