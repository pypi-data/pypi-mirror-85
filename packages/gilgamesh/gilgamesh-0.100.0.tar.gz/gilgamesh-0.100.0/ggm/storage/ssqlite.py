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

import sys, os
import zmq
import asyncio
import sqlite3

from ..lib.kernel import GK
from ..lib.kontext import Kontext

import time
from pprint import pprint

class SSqlite(GK):
    def __init__(self, *args, **kwargs):
        GK.__init__(self, *args, **kwargs)

        self.DB = "ipc:///tmp/series_out"
        self.data_path = kwargs['storage_path']
        try:
            os.makedirs(self.data_path)
        except OSError as e:
            pass

        self.DOUT = "ipc:///tmp/data_out"
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(self.DOUT)
        self.loop.create_task(self.write_data())

        self.loop.create_task(self.query_task())

    async def query_task(self):
        """
        task for answering queries
        """
        dbq = self.context.socket(zmq.REP)
        dbq.connect(self.DB)
        while True:
            raw = await dbq.precv()
            try:
                sig = raw.pop(0)
                dev_id = raw.pop(0)

                db = sqlite3.connect(f'file:{self.data_path}/{dev_id}.db?mode=ro', uri=True)

                if sig in ['get', 'chunk']:
                    db.row_factory = self.get_factory

                cur = db.cursor()
                reply = {}

                if sig == 'measurements':
                    colls = []
                    query = f'SELECT name FROM sqlite_master WHERE type="table"'
                    cur.execute(query)
                    measurements = [i[0] for i in cur.fetchall()]
                    await dbq.psnd(measurements)
                    del measurements
                    cur.close()
                    db.close()
                    continue

                elif sig == 'count':
                    measurement = raw.pop(0)
                    query = f'SELECT count(*) FROM {measurement} '
                    try:
                        tmp = raw.pop(0)
                        if 'start' in tmp.keys():
                            query = query+f"WHERE time > '{tmp['start']}' "
                            if 'stop' in tmp.keys():
                                query = query+f"AND time <= '{tmp['stop']}' "
                    except:
                        pass
                    cur.execute(query)
                    count = [i[0] for i in cur.fetchall()]
                    await dbq.psnd(count)
                    del count
                    cur.close()
                    db.close()
                    continue

                elif sig == 'get':
                    measurement = raw.pop(0)
                    tmp = raw.pop(0)

                    query = f'SELECT * FROM "{measurement}" '

                    if tmp == 'head':
                        query = query+'ORDER BY time DESC LIMIT 1'

                    elif tmp == 'tail':
                        query = query+'ORDER BY time ASC LIMIT 1'

                    elif tmp == 'all':
                        query = query+'ORDER BY time DESC LIMIT 1000'

                    elif isinstance(tmp, dict):
                        if 'start' in tmp.keys():
                            query = query+f"WHERE time > '{tmp['start']}' "
                            if 'stop' in tmp.keys():
                                query = query+f"AND time <= '{tmp['stop']}' "
                        query = query+ f'ORDER BY time DESC LIMIT 1000'

                    else:
                        await dbq.psnd({'Error': True, 'Reason': 'Did not get get!' })
                        continue

                    records = []
                    cur.execute(query)
                    records = cur.fetchall()
                    await dbq.psnd(records)
                    del records
                    cur.close()
                    db.close()
                    continue

                elif sig == 'delete':
                    measurement = raw.pop(0)

                    thresh = self.iso_5min_ago()
                    query = f'SELECT deleteable FROM "{measurement}" where time >= "{thresh}" AND deleteable IS NOT NULL ORDER BY time DESC'
                    cur.execute(query)
                    records = cur.fetchall()
                    if records:
                        query = f'DROP TABLE "{measurement}"'
                        cur.execute(query)
                        db.commit()
                        await dbq.psend_noerr(f'Deletion of {measurement} successful.')
                    else:
                        await dbq.psend_err(f'{measurement} is not deleteable.')

                    del records
                    cur.close()
                    db.close()
                    continue

                elif sig == 'chunk':
                    tic = time.time()
                    measurement = raw.pop(0)
                    tmp = raw.pop(0)

                    try:
                        compression = tmp['compression']
                        offset = tmp['offset']
                        limit = tmp['limit']
                        if 'reverse' in tmp:
                            reverse = tmp['reverse']
                        else:
                            reverse = False
                    except Exception as e:
                        await dbq.psend_err(f'limit/offset or compression parameter missing in chunk query {str(e)}')
                        continue

                    # get table column names and types
                    query = f'PRAGMA table_info({measurement})'
                    cur.execute(query)
                    records = cur.fetchall()
                    clist = [i['tags'] for i in records]

                    cols = []
                    if 'cols' in tmp:
                        clist = ['time']
                        for i in records:
                            if i['name'] in tmp['cols']:
                                clist.append(i['name'])
                        # FIXME sql-injection-city
                        cols_str = [f'"{col}"' for col in clist[1:]]
                        query = f'SELECT time, {", ".join(cols_str)} FROM "{measurement}" '
                    else:
                        query = f'SELECT * FROM "{measurement}" '

                    if 'start' in tmp.keys():
                        query = query+f"WHERE time > '{tmp['start']}' "
                        if 'stop' in tmp.keys():
                            query = query+f"AND time <= '{tmp['stop']}' "

                    if reverse:
                        query = query+ f"ORDER BY time ASC LIMIT {limit} OFFSET {offset}"
                    else:
                        query = query+ f"ORDER BY time DESC LIMIT {limit} OFFSET {offset}"

                    records = []
                    cur.execute(query)
                    records = cur.fetchall()

                    # get last metadata if necessary
                    meta_list = []
                    for c in clist:
                        if c['type'] not in ['TIMESTAMP', 'FLOAT']:
                            meta_list.append(c['name'])

                    if (meta_list and records):
                        if not any(list(records[-1]['tags'].values())):
                            if len(meta_list) > 1:
                                query = f'SELECT {", ".join(meta_list)} FROM "{measurement}" WHERE time < "{records[-1]["time"]}" AND COALESCE({", ".join(meta_list)}) IS NOT NULL ORDER BY time DESC LIMIT 1'
                            else:
                                query = f'SELECT {meta_list[0]} FROM "{measurement}" WHERE time < "{records[-1]["time"]}" AND {meta_list[0]} IS NOT NULL ORDER BY time DESC LIMIT 1'
                            cur.execute(query)
                            meta_data = cur.fetchone()
                            if meta_data:
                                records[-1]['tags'].update(meta_data['tags'])

                    # log slow querys
                    toc = time.time()
                    if toc-tic > 2.00:
                        self.glog.info(f'Slow chunk query ({dev_id} {measurement}): {round((toc-tic), 3)} s')

                    await dbq.psnd(records, compression=compression)
                    del records
                    cur.close()
                    db.close()
                    continue

                else:
                    await dbq.psend_err('SSQLite Driver does not understand.')

            except Exception as e:
                self.glog.error(f'Malformed query? --- {e}')
                #self.glog.error(f'Malformed query? --- {e} --- {sig} {dev_id} {measurement}')
                await dbq.psend_err(str(e))

    async def write_data(self):
        while True:
            raw = await self.receiver.precv()

            try:
                dev_id = raw.pop(0)
                measurement = raw.pop(0)
                data = raw.pop(0)
            except Exception as e:
                self.glog.error(f"Error while parsing incoming Data: {e}")
                continue

            db = sqlite3.connect(f'{self.data_path}/{dev_id}.db', timeout=20)
            cur = db.cursor()
            self.alter_insert(cur, measurement, data)
            db.commit()
            cur.close()
            db.close()

    def alter_insert(self, cur, measurement, data):
        """
        """
        try:
            cur.execute(f'CREATE TABLE IF NOT EXISTS "{measurement}" (time TIMESTAMP)')
        except Exception as e:
            self.glog.error(f"could not create table while inserting: {e}")
            return

        #pprint(data)
        clist = ['time']
        clist_str = ['time']
        try:
            # get table column names and types
            query = f'PRAGMA table_info({measurement})'
            cur.execute(query)
            records = cur.fetchall()
            col_exists = [i[1] for i in records]
        except Exception as e:
            self.glog.error(f"could not get table info while inserting: {e}")
            return

        try:
            for col in data[0]['fields']:
                clist.append(col)
                clist_str.append(f'"{col}"')
                if col not in col_exists:
                    cur.execute(f'ALTER TABLE "{measurement}" ADD COLUMN "{col}" FLOAT')
        except Exception as e:
            self.glog.error(f"could not add missing field while inserting: {e}")
            return

        try:
            for col in data[0]['tags']:
                clist.append(col)
                clist_str.append(f'"{col}"')
                if col not in col_exists:
                    cur.execute(f'ALTER TABLE "{measurement}" ADD COLUMN "{col}" VARCHAR(128)')
        except Exception as e:
            self.glog.error(f"could not add missing tag while inserting: {e}")
            return

        # fkn query
        q = f'INSERT INTO "{measurement}" ' + f"({', '.join(clist_str)}) VALUES ({', '.join([':'+p for p in clist])})"

        data = self.flatten_points(data)

        # fill missing keys
        allkeys = set().union(*data)
        for i in data:
            for missing in allkeys.difference(i):
                i[missing] = None
        try:
            cur.executemany(q, data)
            return
        except Exception as e:
            self.glog.error(f'Could not save data to DB! --- {e}')
            return

    def get_factory(self, cursor, row):
        d = dict()
        d['fields'] = dict()
        d['tags'] = dict()

        for idx, col in enumerate(cursor.description):
            if col[0] == 'time':
                d[col[0]] = row[idx]
            elif isinstance(row[idx], float):
                d['fields'][col[0]] = row[idx]
            elif isinstance(row[idx], str):
                d['tags'][col[0]] = row[idx]
        return d

def ssqlite_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop
    
    ssqlite = SSqlite(**kcfg)
    ssqlite.start()
