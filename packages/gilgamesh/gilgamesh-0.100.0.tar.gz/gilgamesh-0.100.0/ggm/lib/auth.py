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
import socket
import zmq.auth
from zmq.auth.asyncio import AsyncioAuthenticator

from .kontext import Kontext

from pprint import pprint
from time import sleep

class GAuthServer(object):
    """
        TODO: write doc
    """
    def __init__(self, *args, **kwargs):
        from pathlib import Path
        if not 'server_key' in kwargs:
            raise Exception('Nope!')

        keys_dir = kwargs['keys_path']
        public_keys_dir = keys_dir / 'public_keys'
        secret_keys_dir = keys_dir / 'private_keys'

        if not (keys_dir.exists() and
                public_keys_dir.exists() and
                secret_keys_dir.exists()):
            print("CURVE Server: Certificate missing -- this device needs to be comissioned first!")
            print(public_keys_dir, secret_keys_dir)
            sys.exit(1)

        ctx = kwargs['context']
        # Start an authenticator for this context.
        auth = AsyncioAuthenticator(ctx)
        auth.start()
        #auth.allow('127.0.0.1')
        auth.allow()
        # Tell authenticator to use the certificate in a directory
        auth.configure_curve(domain='*', location=public_keys_dir)

        self.server = ctx.socket(zmq.ROUTER)

        server_secret_file = secret_keys_dir / Path(f'{kwargs["server_key"]}.key_secret')
        server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
        self.server.curve_secretkey = server_secret
        self.server.curve_publickey = server_public
        self.server.curve_server = True  # must come before bind
        self.server.bind(f'tcp://*:{kwargs["port"]}')

class GAuthClient(object):
    """
        TODO: write doc
    """
    def __init__(self, *args, **kwargs):
        from pathlib import Path
        if not 'server_key' in kwargs:
            raise Exception('Nope!')
        if not 'client_key' in kwargs:
            raise Exception('Nope!')

        keys_dir = kwargs['keys_path']
        public_keys_dir = keys_dir / 'public_keys'
        secret_keys_dir = keys_dir / 'private_keys'

        if not (keys_dir.exists() and
                public_keys_dir.exists() and
                secret_keys_dir.exists()):
            print("CURVE Server: Certificate missing -- this device needs to be comissioned first!")
            print(public_keys_dir, secret_keys_dir)
            sys.exit(1)

        self.ctx = Kontext()
        self.client = self.ctx.socket(zmq.DEALER)

        client_secret_file = secret_keys_dir / Path(f'{kwargs["client_key"]}.key_secret')
        client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
        self.client.curve_secretkey = client_secret
        self.client.curve_publickey = client_public

        server_public_file = public_keys_dir / Path(f'{kwargs["server_key"]}.key')
        server_public, _ = zmq.auth.load_certificate(server_public_file)
        # The client must know the server's public key to make a CURVE connection.
        self.client.curve_serverkey = server_public
        #woohoo
        retry = 0
        hostname = kwargs['hostname']
        # TODO what if the IP changes?!
        # maybe with setsockopt(zmq.heartbeat) ?
        while True:
            retry+=1
            try:
                ip = socket.gethostbyname(hostname)
                kwargs['ip'] = ip
                self.client.connect(f'tcp://{kwargs["ip"]}:{kwargs["port"]}')
                self.connected = True
                break
            except Exception as e:
                sleep(1)

            if retry == 10:
                self.connected = False
                break
