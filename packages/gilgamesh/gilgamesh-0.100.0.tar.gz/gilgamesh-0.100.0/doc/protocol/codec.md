# zmq
gilgamesh implements a subset of a rest-like api..

## quick
```
send: [ 'greetings' ]
recv: [ 'earthlings' ]
```
```
send: [ 'info' ]
recv: {'dev_id': '<remote_device_id>', 'version': '<remote_gilgamesh_version>'}
```


## json
message format:
```
[ 'json', '<action>', '<collection>', '<document>', '<parameter>' ]
```

collection:
* *collection* name (any sting)

document:
* can be all or a *doc_id* (any sting)

action/parameter:
* get / all, head, tail
  - TODO
* insert / <json_doc>
  - TODO
* nupsert / <json_doc>
  - TODO
* delete / <key>, <'nested', 'key', 'list'>
  - TODO

## series
message format:
```
[ 'series', '<action>', '<database>', '<table>', '<parameter>' ]
```

<database>:
database == device_id of gilgamesh device. SHOULD be unique among
all gilgamesh devices.

table:
table a.k.a. measurement

action/<parameter:
* get / all, head, tail, {'start': '<time>' (, 'stop': '<time>', 'cols': ['<col1>', '<col2>', ... ])}
  - order is descending
  - all has a limit of 1000
  - head gives 'newest' point
  - tail gives 'oldest' point
  - a dict containing time window may also be given
  - stop is optional
* measurements / *noparam*
  - TODO
* count / *noparam*
  - TODO
* upload / *noparam*
  - TODO
* insert / *noparam*
  - TODO
* chunk / *noparam*
  - cols has to be a list of at least one column name
* inventory / *noparam*
  - TODO
* delete / *noparam*
  - deletes a table (needs a column named 'deleteable' with a value set in the last 5 minutes to succeed)
