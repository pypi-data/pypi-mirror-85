# gilgamesh
## Installation instructions for Raspbian Buster

### Install Packages
you may want to install dependencies via apt:
```
sudo apt install python3-zmq python3-blosc python3-ujson
# optional
sudo apt install python3-aiohttp python3-paho-mqtt python3-psycopg2 
```
```
sudo apt install python3-pip
sudo pip install gilgamesh
```

if you want to use TimescaleDB and the builtin mqtt bridge and did not
install the dependencies via apt:
```
sudo pip install gilgamesh[timescaledb,mqtt]
```

### Setup/Configuration
to setup a gilgamesh instance run the following:
```
sudo gilgamesh install
```
the first command copies ggm@.service to /etc/systemd/system and installs
basic configuration templates to /etc/gilgamesh


you may want to edit /etc/gilgamesh/paths.json (e.g. to delete or modify the app path)
```
sudo nano /etc/gilgamesh/paths.json
```

create a device_id
```
sudo gilgamesh gen-id
# or edit by hand
sudo nano /etc/gilgamesh/device_id
```

generate some curvezmq certificates (as user!)
```
gilgamesh gen-cert server
gilgamesh gen-cert client
```

then start with:
```
sudo systemctl start ggm@gateway
```

## Contributing
This project uses [C4(Collective Code Construction Contract)](https://rfc.zeromq.org/spec:42/C4/) process for contributions.
