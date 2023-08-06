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

import ujson, blosc
import asyncio
import zmq.asyncio

class GSock(zmq.asyncio.Socket):
    """A class with some extra serialization methods
        this is the place for the nasty protocol code
        roll your is advised
    """
    BLOSC_ARGS = {
            'typesize': 1,
            'clevel': 5,
            'shuffle': blosc.SHUFFLE,
            'cname': 'blosclz'
    }
    async def psnd(self, msg, compression=False, raw=False):
        """
        """
        if not raw:
            msg = memoryview(ujson.dumps(msg).encode())
        if compression:
            msg = memoryview(blosc.compress(msg, **self.BLOSC_ARGS))

        ret = await self.send(msg, copy=False)
        return ret

    async def precv(self, compression=False, raw=False):
        """
        """
        msg = await self.recv(copy=False)

        if compression:
            msg = memoryview(blosc.decompress(msg))
        if not raw:
            msg = ujson.loads(bytes(msg).decode())

        return msg

    async def dsend(self, msg, z_route=None, compression=False, raw=False):
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

        ret = await self.send_multipart(p, copy=False)
        return ret

    async def drecv(self, compression=False, raw=False):
        """receiving as dealer from dealer(resource worker)
        compatible with req/rep
        """
        rawmsg = await self.recv_multipart(copy=False)
        route = rawmsg[:-1]

        if compression:
            rawmsg[-1] = memoryview(blosc.decompress(rawmsg[-1]))
        if not raw:
            msg = ujson.loads(bytes(rawmsg[-1]).decode())
        else:
            msg = rawmsg[-1]

        return route, msg

    async def upstream(self, cmd, segment, source):

        CHUNK_SIZE = 10000
        PIPELINE = 1

        credit = PIPELINE   # Up to PIPELINE chunks in transit
        total = 0           # Total records received
        chunks = 0          # Total chunks received
        offset = 0          # Offset of next chunk request

        up_cmd = ['series', 'upload']
        up_cmd.extend(cmd[2:])
        up_cmd.append(b'') #FIXME WTF

        # reverse order, so oldest data gets uploaded first
        segment['reverse'] = True
        cmd.append(segment)

        while True:
            while credit:
                segment['offset'] = offset
                segment['limit']= CHUNK_SIZE
                cmd[-1] = segment
                await source.dsend(cmd)
                offset += CHUNK_SIZE
                credit -= 1
            _, msg = await source.drecv(compression=segment['compression'])
            up_cmd[-1] = msg
            if msg:
                await self.dsend(up_cmd)
                _, reply = await self.drecv()
            chunks += 1
            credit += 1
            size = len(msg)
            if size < CHUNK_SIZE:
                break
            # FIXME hack for upload 'flow control'
            await asyncio.sleep(1)

        # 'empty' pipeline
        while credit < PIPELINE:
            _, msg = await source.drecv(compression=segment['compression'])
            up_cmd[-1] = msg
            if msg:
                await self.dsend(up_cmd)
                _, reply = await self.drecv()
            credit += 1
        #!!
        return await asyncio.sleep(0.1)

    async def psend_noerr(self, msg):
        await self.psnd({"Error": False, 'Reason': msg})
    async def dsend_noerr(self, msg, z_route=None):
        await self.dsend({"Error": False, 'Reason': msg}, z_route)
    async def psend_err(self, errmsg):
        await self.psnd({"Error": True, 'Reason': errmsg})
    async def dsend_err(self, errmsg, z_route=None):
        await self.dsend({"Error": True, 'Reason': errmsg}, z_route)

class Kontext(zmq.asyncio.Context):
    _socket_class = GSock
