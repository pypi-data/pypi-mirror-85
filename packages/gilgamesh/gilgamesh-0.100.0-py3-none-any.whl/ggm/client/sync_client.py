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

import sys, time, zmq
import pandas as pd
import numpy as np
from .auth import AuthClient
from ..lib.sync_context import Kontext
from multiprocessing import Process

import datetime
from datetime import datetime as dt

from pprint import pprint
from time import sleep

class GClient(AuthClient):
    def __init__(self, ggm_host='local',*args, **kwargs):
        """GILGAMESH™ Client
        
        synchronous gilgamesh client for jupyter noetbooks
        
        Parameters
        ----------
        ggm_host: str
            found as key in $HOME/.gilgamesh/config/client_config.json

        Returns
        -------
        class GClient

        Examples
        --------
        >>> ggm = GClient()
        Connecting to gilgamesh successful!
        >>> ggm.full_cfg
        {'gilgamesh': {
            'hostname': 'gilgamesh.server',
            'port': 6001,
            'server_key': 'server',
            'client_key': 'client',
        'my_gatway': {
            'ip': '127.0.0.1',
            'port': 6001,
            'server_key': 'gateway',
            'client_key': 'client'}
        }
        >>> print(ggm.get_store())
        <large_dict>


        """
        self.version = '0.9'
        self.ggm_host = ggm_host
        super().__init__(ggm_host, *args, **kwargs)

        self.client = self.get_client()

        self.poller = zmq.Poller()
        self.poller.register(self.client, zmq.POLLIN)

        assert self.check_conn()
        
        self.client.psend(['info'])
        reply = self.client.precv()
        self.remote_dev_id = reply['dev_id']
        
    def show_devices(self, print_table=False):
        """
        gives a list of all known devices on gilgamesh

        Optional:
        print all devices in store and their associated tables
        as markdown table in jupyter notebook

        Parameters
        ----------
        print_table: bool
            whether or not to print a markdown formatted table

        Returns
        -------
        list of device names

        See Also
        --------
        GClient.show_measurements()

        Examples
        --------
        >>> d = GClient.show_devices()
        <Markdown Table>

        >>> print(d)
        ['dev1', 'dev2']

        """
        from IPython.display import display, Markdown
        md = f'Device Id | Table(s)/Measurement(s)  \n'
        md += f':--- | :---: \n'

        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()

        own_tables = reply['device_state_db'][self.remote_dev_id]['inventory']
        md += f"{self.remote_dev_id} | {list(own_tables.keys())}\n"

        store = reply['device_state_db'][self.remote_dev_id]['store']
        for dev in store:
            md += f"{dev} | {[t for t in store[dev].keys()]} \n"

        if print_table:
            display(Markdown(md))

        devs = [t for t in store.keys()]
        devs.extend([self.remote_dev_id])
        return devs

    def show_measurements(self, device, print_table=False):
        """
        gives a list of all tables/measurements from specified device

        Optional:
        print all tables, their timeframe and number of records
        in store for specified device as markdown table in jupyter notebook

        Parameters
        ----------
        dev_id: str
            device identifier

        print_table: bool
            whether or not to print a markdown formatted table

        Returns
        -------
        list of table/measurement names

        See Also
        --------
        GClient.show_devices()

        Examples
        --------
        >>> m = GClient.show_measurements()
        <Markdown Table>

        >>> print(m)
        ['table1', 'table2']

        """
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()

        from IPython.display import display, Markdown
        md = f'Table/Measurement | Start | Stop | Count \n'
        md += f':---| --- | --- | --- \n'

        if device == self.remote_dev_id:
            data = reply['device_state_db'][self.remote_dev_id]['inventory']
        else:
            data = reply['device_state_db'][self.remote_dev_id]['store'][device]

        for table in data.keys():
            cmd = ['series', 'count', device, table]
            self.client.psend(cmd)
            rep = self.client.precv()
            start = data[table]['tail']['time']
            stop = data[table]['head']['time']
            md += f"{table} | {start} | {stop} | {rep[0]}\n"

        if print_table:
            display(Markdown(md))

        return [t for t in data.keys()]
    
    def get_store(self):
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()
        store = reply['device_state_db'][self.remote_dev_id]['store']
        store[self.remote_dev_id] = reply['device_state_db'][self.remote_dev_id]['inventory']
        return store


    def get_measurement(self, dev_id, table, start, stop=None, cols=None, progress=True, dataframe=True):
        """
        get measurement from gilgamesh

        starts download process

        Parameters
        ----------
        dev_id: str
            device identifier

        table: str
            table/measurement from/on the device

        start: pd.DateTime str
            pandas parsable datetime string
            e.g.: "2000-01-01 12:00:04.933355" or "2000-01-01"

        stop: DateTime str
            Optional:
                same as start

        cols: list of strings
            Optional:
                list of column names; if not given selects all columns

        progress: bool
            - print updates on download procgress
            - defaults to True

        dataframe: bool
            - return pd.DataFrame
            - defaults to True


        Returns
        -------
        pd.DataFrame with DateTime index
        or
        list of dicts

        See Also
        --------
        GClient

        Examples
        --------
        >>> dF = GClient.get_measurement('my_device',
                                         'table',
                                         start='2000-01-01 12:00:00',
                                         stop='2000-01-01 12:00:10',
                                         progress=False)

        -- my_device table --
        Downloading chunk 1/1
        2 records received.
        Time elapsed: 0.1 s

        >>> print(dF)
                                        field   tag
        time
        2000-01-01 12:00:04.933355  1240574.0   'u'
        2000-01-01 12:00:08.123555  1240674.0   'v'

        >>> GClient.get_measurement('my_device',
                                    'table',
                                    start='2000-01-01 12:00:00',
                                    stop='2000-01-01 12:00:10',
                                    progress=False,
                                    dataframe=False)

        [{'fields': {'field': 1240574.0}, 'tags': {'tag', 'u'}, 'time': '2000-01-19 12:00:04.933355'},
        {'fields': {'field': 1240674.0}, 'tags': {'tag', 'v'}, 'time':  '2000-01-19 12:00:08.123555'}]


        """
        nproc = 4
        pipeline = 10
        chunk_size = 5000
        compression = True

        params = dict()

        params['start'] = start
        params['stop'] = stop or self.get_tmst_now()

        if cols:
            params['cols'] = cols

        params['compression'] = compression

        # compression will be ignored here
        count_cmd = ['series', 'count', dev_id, table, params]
        self.client.psend(count_cmd)
        count_all = self.client.precv()
        chunk_count = count_all[0] / chunk_size
        nproc = int(chunk_count) // pipeline + (chunk_count % pipeline > 0)
        if nproc > 4:
            nproc = 4

        try:
            put_work = self.ctx.socket(zmq.PUSH)
            put_work.setsockopt(zmq.LINGER, 0)
            put_work.bind('ipc://@work')

            res = self.ctx.socket(zmq.PULL)
            res.setsockopt(zmq.LINGER, 0)
            res.bind('ipc://@result')

            for proc in range(nproc):
                Process(target=GDownloader, args=(self.ggm_host, pipeline, chunk_size, dataframe)).start()

            # uncool
            sleep(1)

            print(f'-- {dev_id} {table} --')
            seg_td = (pd.to_datetime(params['stop'])-pd.to_datetime(params['start']))/nproc
            params['stop'] = (pd.to_datetime(params['start'])+seg_td).isoformat(sep=' ')
            data = []
            total_chunks = 0
            tic = time.time()

            for p in range(nproc):
                count_cmd = ['series', 'count', dev_id, table, params]
                self.client.psend(count_cmd)
                raw = self.client.precv()
                count_all = raw.pop()
                total_chunks += count_all // chunk_size + (count_all % chunk_size > 0)

                cmd = ['series', 'chunk', dev_id, table, params]
                put_work.psend(cmd)
                params['start'] = params['stop']
                params['stop'] = (pd.to_datetime(params['stop'])+seg_td).isoformat(sep=' ')


            chnk = 0
            while True:
                if chnk == total_chunks:
                    break
                tmp = res.precv()
                if dataframe:
                    tmp = pd.DataFrame.from_records(tmp, index='time')
                    tmp.index = pd.to_datetime(tmp.index)
                    data.append(tmp)
                else:
                    data.extend(tmp)
                chnk += 1
                if progress:
                    self.update_progress(chnk, total_chunks)

            if dataframe and data:
                data = pd.concat(data, sort=False)
                data.sort_index(inplace=True, ascending=True)
                # ffill 'object' cols
                tcol = list({col: typ for (col, typ) in dict(data.dtypes).items() if typ==np.dtype('O')})
                data.loc[:,tcol] = data.loc[:,tcol].ffill()
            toc = time.time()
            print(f'\n{len(data)} records received.')
            print(f'Time elapsed: {round(toc-tic, 2)} s')
        except Exception as e:
            print(f'Error while downloading {dev_id} {table} ({e})')
            data = self.clean_pipeline()
        except KeyboardInterrupt:
            data = self.clean_pipeline()
        finally:
            put_work.close()
            res.close()

        return data

    def get_tmst_now(self):
        return dt.utcnow().isoformat(sep=' ')

    def clean_pipeline(self):
        msg = []
        while len(dict(self.poller.poll(1000))) > 0:
            _, msg = self.client.drecv(raw=True)
        if isinstance(msg, dict):
            if 'Reason' in msg.keys():
                pprint(msg['Reason'])
        return True

    def update_progress(self, chunk, total):
        sys.stdout.write(f'\rDownloading chunk {chunk}/{total}')
        sys.stdout.flush()

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

class GAbo(object):
    def __init__(self):
        self.ctx = Kontext()
        poller = zmq.Poller()

        self.local_frontend = self.ctx.socket(zmq.DEALER)
        self.local_frontend.setsockopt(zmq.LINGER, 0)
        self.local_frontend.connect('ipc:///tmp/frontend')

        poller.register(self.local_frontend, zmq.POLLIN)

        self.local_frontend.psend(['info'])
        socks = dict(poller.poll(100))
        if not socks.get(self.local_frontend) == zmq.POLLIN:
            self.local_frontend.close()
            raise Exception('is local gilgamesh instance running?')

        socks = dict(poller.poll(100))
        if socks.get(self.local_frontend) == zmq.POLLIN:
            raw = self.local_frontend.precv()
            fro_dev_id = raw['dev_id']

        poller.unregister(self.local_frontend)

        self.abo_query = self.ctx.socket(zmq.DEALER)
        self.abo_query.setsockopt(zmq.LINGER, 0)
        self.abo_query.connect('ipc:///tmp/abo_front')

        poller.register(self.abo_query, zmq.POLLIN)

        self.abo_query.psend(['device_id'])
        socks = dict(poller.poll(100))
        if not socks.get(self.abo_query) == zmq.POLLIN:
            raise Exception('is local abo running?')

        socks = dict(poller.poll(100))
        if socks.get(self.abo_query) == zmq.POLLIN:
            dev_id = self.abo_query.precv()

        poller.unregister(self.abo_query)

        if not dev_id == fro_dev_id:
            raise Exception(f'setup appears to be malicious: ggm dev_id: {fro_dev_id} vs abo dev_id: {dev_id}')

        self.dev_id = dev_id

    def show_abos(self):
        cmd = ['json', 'get',  'abo_db', self.dev_id, 'head']
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response['abo_db'][self.dev_id])

    def delete_abo(self, dev, table):
        cmd = ['json', 'delete',  'abo_db', self.dev_id, dev, table]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def clear_abos(self):
        cmd = ['json', 'delete',  'abo_db', self.dev_id]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def add_abo(self, abos):
        cmd = ['json', 'nupsert', 'abo_db', self.dev_id, abos]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def get_local(self, dev_id, table, start=None, stop=None, cols=None):
        """
        method for getting local hdf files downloaded by 'local abo' app
        """
        if not start:
            return 'error: start must be given'

        self.abo_query.dsend(['path', dev_id, table])
        _, path = self.abo_query.drecv()

        if not path:
            return 'does not exist, or is not yet downloaded -- please check abo'
        print(f'loading from: {path}')

        query = f"index >= '{start}' "
        if stop:
            query += "and index <= '{stop}'"
        with pd.HDFStore(path, mode='r') as store:
            df = store.select('', where=query)
        data.sort_index(inplace=True, ascending=True)
        # ffill 'object' cols
        tcol = list({col: typ for (col, typ) in dict(data.dtypes).items() if typ==np.dtype('O')})
        data.loc[:,tcol] = data.loc[:,tcol].ffill()
        return df

    def terminate(self):
        self.local_frontend.close()
        self.abo_query.close()
        self.ctx.term()
        print(f'Terminated Abo Client')

class GDownloader(AuthClient):
    def __init__(self, ggm_host, pipeline, chunk_size, dataframe, *args, **kwargs):
        super().__init__(ggm_host, *args, **kwargs)

        self.pipeline = pipeline
        self.chunk_size = chunk_size
        self.dataframe = dataframe

        self.client = self.get_client()

        self.get_work = self.ctx.socket(zmq.PULL)
        self.get_work.setsockopt(zmq.LINGER, 0)
        self.get_work.connect('ipc://@work')

        self.res = self.ctx.socket(zmq.PUSH)
        self.res.setsockopt(zmq.LINGER, 0)
        self.res.connect('ipc://@result')

        self.work_loop()

    def work_loop(self):
        try:
            fullcmd = self.get_work.precv()
            self.download(fullcmd[:-1], fullcmd[-1])
        finally:
            self.terminate()

    def download(self, cmd, params):

        CHUNK_SIZE = self.chunk_size
        PIPELINE = self.pipeline

        credit = PIPELINE   # Up to PIPELINE chunks in transit
        total = 0           # Total records received
        chunks = 0          # Total chunks received
        offset = 0          # Offset of next chunk request
        cmd.append(params)

        while True:
            while credit:
                params['offset'] = offset
                params['limit']= CHUNK_SIZE
                cmd[-1] = params
                self.client.dsend(cmd)
                offset += CHUNK_SIZE
                credit -= 1
            route, msg = self.client.drecv(compression=params['compression'])
            if len(msg) > 0:
                if self.dataframe:
                    msg = self.flatten_points(msg)
                self.res.psend(msg)
            chunks += 1
            credit += 1
            size = len(msg)
            if size < CHUNK_SIZE:
                break

        # 'empty' pipeline
        while credit < PIPELINE:
            route, msg = self.client.drecv(compression=params['compression'])
            credit += 1
            if len(msg) > 0:
                if self.dataframe:
                    msg = self.flatten_points(msg)
                self.res.psend(msg)

    def flatten_points(self, data):
        """
        takes list of data dicts and flattens it
        if field and tag names are identical, tags wil get overwritten by fields
        """
        for d in data:
            d.update(d['tags'])
            d.update(d['fields'])
            if isinstance(d['tags'], dict):
                del d['tags']
            if isinstance(d['fields'], dict):
                del d['fields']
        return data

    def terminate(self):
        self.get_work.close()
        self.res.close()
        self.client.close()
        self.ctx.term()
        sys.exit(0)
