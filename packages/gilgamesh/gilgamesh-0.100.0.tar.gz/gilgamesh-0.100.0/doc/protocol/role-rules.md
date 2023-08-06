role rules:
===

Client
```
MUST		-

SHOULD		upstream

MUST NOT	downstream

SHOULD NOT	storage
SHOULD NOT	http_api
SHOULD NOT	mqtt_bridge
```

Gateway
```
MUST		http_api
MUST		upstream
MUST		downstream

MUST NOT	-

OPTIONAL	storage
OPTIONAL	mqtt_bridge
```

Server
```
MUST		http_api
MUST		downstream
MUST		storage

MUST NOT	upstream

OPTIONAL	mqtt_bridge
```
