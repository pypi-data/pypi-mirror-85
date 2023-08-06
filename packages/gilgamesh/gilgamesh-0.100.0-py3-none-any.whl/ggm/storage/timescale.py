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

import psycopg2
import psycopg2.extras
from psycopg2 import sql

from ..lib.kernel import GK
from ..lib.kontext import Kontext

import time
import json
from pprint import pprint
from datetime import datetime as dt

class KTimescale(GK):
    def __init__(self, *args, **kwargs):
        GK.__init__(self, *args, **kwargs)

        self.DB = "ipc:///tmp/series_out"

        # FIXME hard coded? better for secrets?
        with open(f'/etc/gilgamesh/timescaledb.secret', 'r') as raw:
            dbcfg = json.load(raw)
            dbname = dbcfg['dbname']
            dbuser = dbcfg['dbuser']
            dbpw = dbcfg['dbpw']
            dbhost = dbcfg['dbhost']
            del dbcfg

        self.dsn = f'dbname={dbname} user={dbuser} password={dbpw} host={dbhost}'
        tmst_as_string = psycopg2.extensions.new_type((1114,), 'DATETIME', psycopg2.STRING)
        psycopg2.extensions.register_type(tmst_as_string)

        # we are a time series adapter!
        self.DOUT = "ipc:///tmp/data_out"
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(self.DOUT)

        self.loop.create_task(self.write_data())
        self.loop.create_task(self.query_task())

    async def query_task(self):
        """
        task for answering timescaledb queries
        """
        dbq = self.context.socket(zmq.REP)
        dbq.connect(self.DB)
        conn = psycopg2.connect(self.dsn, cursor_factory=psycopg2.extras.RealDictCursor)
        conn.set_session(autocommit=True, readonly=True)
        cur = conn.cursor()
        while True:
            raw = await dbq.precv()
            try:
                sig = raw.pop(0)
                dev_id = raw.pop(0)

                #print(sig)
                #pprint(raw)
                if sig == 'measurements':
                    colls = []
                    query = sql.SQL("SELECT table_name FROM information_schema.tables WHERE table_schema = {0}").format(sql.Literal(dev_id))
                    cur.execute(query)
                    records = [r['table_name'] for r in cur.fetchall()]
                    await dbq.psnd(records)
                    continue

                elif sig == 'count':
                    measurement = raw.pop(0)
                    query = sql.SQL("SELECT COUNT(*) FROM {0}.{1} ").format(*tuple(map(sql.Identifier, [dev_id, measurement])))

                    try:
                        tmp = raw.pop(0)
                        if 'start' in tmp.keys():
                            query = query + sql.SQL(f"WHERE time > '{tmp['start']}' ")
                            if 'stop' in tmp.keys():
                                query = query + sql.SQL(f"AND time <= '{tmp['stop']}' ")
                    except:
                        pass

                    cur.execute(query)
                    records = cur.fetchone()
                    await dbq.psnd([records['count']])
                    continue

                elif sig == 'get':
                    measurement = raw.pop(0)
                    tmp = raw.pop(0)

                    query = sql.SQL("SELECT * FROM {0}.{1} ").format(*tuple(map(sql.Identifier, [dev_id, measurement])))
                    if tmp == 'head':
                        query = query + sql.SQL('ORDER BY time DESC LIMIT 1')
                    elif tmp == 'tail':
                        query = query + sql.SQL('ORDER BY time ASC LIMIT 1')
                    elif tmp == 'all':
                        query = query + sql.SQL('ORDER BY time DESC LIMIT 1000')
                    elif isinstance(tmp, dict):
                        if 'start' in tmp.keys():
                            query = query + sql.SQL(f"WHERE time > '{tmp['start']}' ")
                            if 'stop' in tmp.keys():
                                query = query + sql.SQL(f"AND time <= '{tmp['stop']}' ")
                        query = sql.Composed(query, 'ORDER BY time DESC LIMIT 1000')
                    else:
                        await dbq.psend_err(f'malicious get query.')
                        continue

                    cur.execute(query)
                    records = cur.fetchall()
                    records = self.from_db_format(records)
                    if records is None:
                        records = []
                    await dbq.psnd(records)
                    continue

                elif sig == 'delete':
                    measurement = raw.pop(0)

                    thresh = self.iso_5min_ago().isoformat(sep=' ')
                    query = sql.SQL("SELECT EXISTS(SELECT deleteable FROM {0}.{1} where time >= {2} AND deleteable IS NOT NULL ORDER BY time DESC)").format(
                            sql.Identifier(dev_id), sql.Identifier(measurement), sql.Literal(thresh))
                    cur.execute(query)
                    records = cur.fetchall()
                    if records[0][0]:
                        query = sql.SQL("DROP TABLE {0}.{1} CASCADE").format(
                                sql.Identifier(dev_id), sql.Identifier(measurement))
                        cur.execute(query)
                        await dbq.psend_noerr(f'Deletion of {measurement} successful.')
                    else:
                        await dbq.psend_err(f'{measurement} is not deleteable.')

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

                    query = sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = {0} AND table_name = {1}").format(sql.Literal(dev_id),sql.Literal(measurement))
                    cur.execute(query)
                    records = cur.fetchall()
                    meta_list = [x['column_name'] for x in filter(lambda x: x['data_type'] == 'character varying', records)]

                    clist = []
                    if 'cols' in tmp:
                        for i in records:
                            if i['column_name'] == 'time':
                                clist.append(i[0])
                            elif i['column_name'] in tmp['cols']:
                                clist.append(i[0])

                        query = sql.SQL("SELECT {2} FROM {0}.{1} ").format(
                                *tuple(map(sql.Identifier, [dev_id, measurement])),
                                sql.SQL(', ').join(map(sql.Identifier, clist)))
                    else:
                        clist = [n['column_name'] for n in records]
                        query = sql.SQL("SELECT * FROM {0}.{1} ").format(
                                sql.Identifier(dev_id), sql.Identifier(measurement))

                    # FIXME sql-injection-city
                    if 'start' in tmp.keys():
                        query = query + sql.SQL(f"WHERE time > '{tmp['start']}' ")
                        if 'stop' in tmp.keys():
                            query = query + sql.SQL(f"AND time <= '{tmp['stop']}' ")

                    if reverse:
                        query = query + sql.SQL(f"ORDER BY time ASC LIMIT {limit} OFFSET {offset}")
                    else:
                        query = query + sql.SQL(f"ORDER BY time DESC LIMIT {limit} OFFSET {offset}")

                    records = []
                    cur.execute(query)
                    records = cur.fetchall()
                    records = self.from_db_format(records)

                    # get last metadata if necessary
                    if (meta_list and records):
                        if not any(list(records[-1]['tags'].values())):
                            if len(meta_list) > 1:
                                query = sql.SQL("SELECT {0} FROM {1}.{2} WHERE time < {3} AND COALESCE({0}) IS NOT NULL ORDER BY time DESC LIMIT 1").format(
                                        sql.SQL(', ').join(map(sql.Identifier, meta_list)),
                                        *tuple(map(sql.Identifier, [dev_id, measurement])),
                                        sql.Literal(records[-1]['time']))
                            else:
                                query = sql.SQL("SELECT {0} FROM {1}.{2} WHERE time < {3} AND {0} IS NOT NULL ORDER BY time DESC LIMIT 1").format(
                                        sql.Identifier(meta_list[0]),
                                        *tuple(map(sql.Identifier, [dev_id, measurement])),
                                        sql.Literal(records[-1]['time']))
                            cur.execute(query)
                            meta_data = cur.fetchone()
                            if meta_data:
                                records[-1]['tags'] = meta_data

                    # log slow querys
                    toc = time.time()
                    if toc-tic > 2.00:
                        self.glog.info(f'Slow chunk query ({dev_id} {measurement}): {round((toc-tic), 3)} s')
                    tic = time.time()

                    await dbq.psnd(records, compression=compression)
                    continue

                else:
                    await dbq.psnd({'Error': True, 'Reason': 'TimescaleDB Driver does not understand.'})

            except Exception as e:
                self.glog.error(f'Malformed query? -- {e}')
                await dbq.psend_err(str(e))

    async def write_data(self):
        conn = psycopg2.connect(self.dsn, cursor_factory=psycopg2.extras.RealDictCursor)
        conn.set_session(autocommit=True) # autocommit
        conn.set_isolation_level(0) # autocommit
        cur = conn.cursor()
        while True:
            raw = await self.receiver.precv()

            try:
                dev_id = raw.pop(0)
                measurement = raw.pop(0)
                data = raw.pop(0)
            except Exception as e:
                self.glog.error(f"Error while parsing incoming Data: {e}")
                continue

            self.alter_insert(cur, dev_id, measurement, data)

    def alter_insert(self, cur, dev_id, measurement, data):
        """
        """
        try:
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {0}").format(sql.Identifier(dev_id)))
            cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {0}.{1} (time TIMESTAMP)").format(
                *tuple(map(sql.Identifier, [dev_id, measurement]))))
            cur.execute(sql.SQL("SELECT create_hypertable('{0}.{1}', 'time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE)").format(
                *tuple(map(sql.Identifier, [dev_id, measurement]))))
        except Exception as e:
            self.glog.error(f"error creating hypertable: {e}")
            return

        query = sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = {0} AND table_name = {1}").format(sql.Literal(dev_id),sql.Literal(measurement))
        cur.execute(query)
        records = cur.fetchall()
        col_exists = [x['column_name'] for x in records]

        clist = ['time']
        try:
            for col in data[0]['fields']:
                clist.append(col)
                if col not in col_exists:
                    cur.execute(sql.SQL('ALTER TABLE {0}.{1} ADD COLUMN IF NOT EXISTS {2} FLOAT DEFAULT NULL').format(
                        *tuple(map(sql.Identifier, [dev_id, measurement, col]))))
        except Exception as e:
            self.glog.error(f"could not add missing field while inserting: {e}")
            return

        try:
            for col in data[0]['tags']:
                clist.append(col)
                if col not in col_exists:
                    cur.execute(sql.SQL('ALTER TABLE {0}.{1} ADD COLUMN IF NOT EXISTS {2} VARCHAR(128) DEFAULT NULL').format(
                        *tuple(map(sql.Identifier, [dev_id, measurement, col]))))
        except Exception as e:
            self.glog.error(f"could not add missing tag while inserting: {e}")
            return


        # fkn query
        q = sql.SQL("INSERT INTO {0}.{1} ({2}) VALUES %s").format(
                *tuple(map(sql.Identifier, [dev_id, measurement])),
                sql.SQL(', ').join(map(sql.Identifier, clist)))
        placeholder = sql.SQL("({0})").format(
                sql.SQL(', ').join(map(sql.Placeholder, clist)))
        data = self.flatten_points(data)

        # fill missing keys
        allkeys = set().union(*data)
        for i in data:
            for missing in allkeys.difference(i):
                i[missing] = None
        try:
            psycopg2.extras.execute_values(cur, q, data, template=placeholder)
            return
        except Exception as e:
            self.glog.error(f'Could not save data to DB! --- {e} --- {dev_id} {measurement} length: {len(data)}')
            return

    def from_db_format(self, data):
        """
        takes list of data dicts
        returns list of data dicts where float/str values are
        split into fields/tags
        """
        if not data:
            return []
        keys = data[0].keys()
        for i, d in enumerate(data):
            tmp = {}
            tmp['fields'] = {}
            tmp['tags'] = {}
            for k in keys:
                if k == 'time':
                    tmp[k] = d[k]
                elif isinstance(d[k], float) or isinstance(d[k], int):
                    tmp['fields'][k] = d[k]
                elif isinstance(d[k], str):
                    tmp['tags'][k] = d[k]
            data[i] = tmp
        return data

def timescale_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop
    
    timescale = KTimescale(**kcfg)
    timescale.start()
