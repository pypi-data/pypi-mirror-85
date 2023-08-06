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

from pathlib import Path
import json, socket, zmq.auth
from ..lib.sync_context import Kontext

class AuthClient(object):
    def __init__(self, ggm_host, *args, **kwargs):
        """
        gna
        """
        cfg_file = Path.home()/'.gilgamesh'/'config'/'client_config.json'
        if not cfg_file.exists():
            raise FileNotFoundError(f'{cfg_file} does not exist.')
        
        with open(cfg_file, 'r') as raw:
            cfg = json.load(raw)
            self.cfg_full = cfg
        
        if not ggm_host in cfg:
            raise ValueError(f'{ggm_host} not found in config.')

        cfg = cfg[ggm_host]
        
        self.ctx = Kontext()
        
        keys_path = Path.home()/'.gilgamesh'/'keys'
        client_secret_file = keys_path/'private_keys'/f'{cfg["client_key"]}.key_secret'
        server_public_file = keys_path/'public_keys'/f'{cfg["server_key"]}.key'
        
        self.client_public, self.client_secret = zmq.auth.load_certificate(client_secret_file)
        self.server_public, _ = zmq.auth.load_certificate(server_public_file)
        
        if not 'ip' in cfg:
            try:
                ip = socket.gethostbyname(cfg['hostname'])
                cfg['ip'] = ip
            except:
                raise ConnectionError(f'Could not resolve {hostname}')

        self.host_ip = cfg['ip']
        self.host_port = cfg['port']

    def get_client(self):
        client = self.ctx.socket(zmq.DEALER)
        client.setsockopt(zmq.LINGER, 0)

        client.curve_secretkey = self.client_secret
        client.curve_publickey = self.client_public
        client.curve_serverkey = self.server_public

        client.connect(f'tcp://{self.host_ip}:{self.host_port}')
        return client
