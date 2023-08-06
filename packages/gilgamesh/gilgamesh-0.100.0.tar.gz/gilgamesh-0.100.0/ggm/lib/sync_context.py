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

import zmq, ujson, blosc

class GSock(zmq.Socket):
    """A class with some extra serialization methods
    
    """
    BLOSC_ARGS = {
            'typesize': 1,
            'clevel': 5,
            'shuffle': blosc.SHUFFLE,
            'cname': 'blosclz'
    }
    def psend(self, msg, compression=False, raw=False):
        """
        """
        if not raw:
            msg = memoryview(ujson.dumps(msg).encode())
        if compression:
            msg = memoryview(blosc.compress(msg, **self.BLOSC_ARGS))

        ret = self.send(msg, copy=False)
        return ret

    def precv(self, compression=False, raw=False):
        """
        """
        msg = self.recv(copy=False)

        if compression:
            msg = memoryview(blosc.decompress(msg))
        if not raw:
            msg = ujson.loads(bytes(msg).decode())

        return msg

    def dsend(self, msg, z_route=None, compression=False, raw=False):
        """
        sending as dealer to dealer (resource worker/client/...)

        emtpy frame for compatibility with req/rep OR zmq internal route
        """
        p = z_route or [b'']

        if not raw:
            msg = memoryview(ujson.dumps(msg).encode())
        if compression:
            msg = memoryview(blosc.compress(msg, **self.BLOSC_ARGS))

        p.append(msg)

        ret = self.send_multipart(p, copy=False)
        return ret

    def drecv(self, compression=False, raw=False):
        """receiving as dealer from dealer(resource worker)
        compatible with req/rep
        """
        rawmsg = self.recv_multipart(copy=False)
        route = rawmsg[:-1]

        if compression:
            rawmsg[-1] = memoryview(blosc.decompress(rawmsg[-1]))
        if not raw:
            msg = ujson.loads(bytes(rawmsg[-1]).decode())
        else:
            msg = rawmsg[-1]

        return route, msg

class Kontext(zmq.Context):
    _socket_class = GSock
