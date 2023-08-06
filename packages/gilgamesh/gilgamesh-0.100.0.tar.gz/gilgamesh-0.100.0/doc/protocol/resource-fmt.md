resource structure for series data:
===
```
<device_id>: # database
{
    <resource_id>: # table
    {
        [
            {
                'time': <tmst>,
                'fields':
                {
                    <val_name0>: <value>,
                    <val_name1>: <value>
                    ...
                },
                'tags':
                {
                    'unit': <unit>,
                    'tags': <tags>,
                    'meta': <meta>
                    ...
                }
            },
            {
                ...
            }
        ]
    }
}
```

resource structure for JSON data:
===
```
<db_name>: # 'database'
{
    <collection>: # collection/table
    {
        <DB_obj>: # db index/rowid
        {
            <JSON_str>
        }
    }
}
```
