# radio_api

Simple mplayer-based radio player controllable via REST API

## Overview

Stations are stored with their **URL** in a **SQLite** database.

## Requirements

For using this application, you will need:

- Python 3
- Flask
- SQLite 3

## Docker container

There is a [`Dockerfile`](Dockerfile) for running this application inside a container based on [Ubuntu Linux](https://www.ubuntu.com).
To create the image, run the following command:

```shell
$ docker build -t radio .
```

This will take a couple of minutes, afterwards you should see the image:
```shell
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
radio               latest              84572d3b8826        1 hour ago          504.8MB
...
```

To start a new container based on this image, execute:

```shell
$ docker run -d -p 5000:5000 radio
b4735f102afb6e288b0a35d17b0e63da4d6bd2652467709c5c28538088ae5d30

$ docker ps
CONTAINER ID        IMAGE                      COMMAND                   CREATED             STATUS                PORTS                                                                                                  NAMES
b4735f102afb        radio                      "/bin/sh -c \"/opt/jo…"   16 seconds ago      Up 14 seconds         0.0.0.0:5000->5000/tcp                                                                                 boring_chebyshev
...
```

It is also possible to use shipped [docker-compose file](docker-compose.yml):

```shell
$ docker-compose create
$ docker-compose up
Starting radio ... done
Attaching to radio
...
radio       |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## API calls

There is also a pre-defined [Postman collection](postman.json).

| Call | Method | Parameters | Description |
| ---- | ------ | ---------- | ----------- |
| `/api/stations` | `GET` | - | returns all available stations |
| `/api/stations/<id/name>` | `GET` | station ID or name | returns a particular station |
| `/api/stations/<id/name>/play` | `GET` | station ID or name | plays a particular station |
| `/api/stations` | `POST` | `{ "item": { "url": "<str>" } }` | creates a new station |
| `/api/stations/<id/name>` | `PUT,POST` | station ID or name, `{ "item": {"id": <int>, "url": "<str>"} }` | updates an existing station |
| `/api/stations/<id/name>` | `DELETE` | station ID or name | removes a station |
| `/api/next` | `GET` | - | plays the next station |
| `/api/previous` | `GET` | - | plays the previous station |
| `/api/stop` | `GET` | - | stops the radio |
| `/api/current` | `GET` | - | returns the currently played station |
| `/api/volume` | `GET` | - | returns the current volume level |
| `/api/volume` | `POST` | `{ "level": <int> }` | sets volume to a specific level |
| `/api/volume/up` | `GET` | - | increases the volume by 10% |
| `/api/volume/down` | `GET` | - | decreases the volume by 10% |

## Database layout

### `stations`

| Field name | Field type | Description |
| ---------- | ---------- | ----------- |
| `station_id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | station ID |
| `station_name` | `TEXT NOT NULL` | station name |
| `station_url` | `TEXT NOT NULL` | station URL |
