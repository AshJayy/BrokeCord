# Python CLI Socket Applications

This repository contains three Python networking projects, each demonstrating a different communication pattern:

1. `t1-client-server`: Basic client-server messaging.
2. `t2-pub-sub`: Publisher-Subscriber (Pub-Sub) chat system.
3. `t3-topic-filtering`: Pub-Sub with topic-based message filtering.

## Client Server

`cd t1-client-server`

### Description
A simple client-server application using Python sockets. The server accepts a connection from a single client and relays messages.

### Features
- Client can connect to the server.
- Client can send and receive messages.
- Graceful disconnects.

### Usage
Start the server:
```bash
python3 t1-client-server/server.py <port>
```

Start a client:
```bash
python3 t1-client-server/client.py <port>
```

## Publisher-Subscriber (Pub-Sub)

`cd t2-pub-sub`

### Description
A terminal-based chat system using the Publisher-Subscriber (Pub-Sub) model. Users can join as either publishers (mods) or subscribers (members).

### Features
- Choose between publisher or subscriber roles.
- Real-time message delivery for subscribers.
- Graceful Exit.

### Usage
Start the server:
```bash
python3 t2-pub-sub/server.py <port>
```

Start a client:
```bash
python3 t2-pub-sub/client.py <port> <PUBLISHER|SUBSCRIBER>
```

## Publisher-Subscriber with Topic Filtering

`cd t3-topic-filtering`

### Description
An advanced Pub-Sub system that introduces topic-based message filtering. Subscribers only receive messages relevant to their chosen topic.

### Features
- Topic selection and filtering.
- Publisher and subscriber roles.

### Usage
Start the server:
```bash
python3 t3-topic-filtering/server.py <port>
```

Start a client:
```bash
python3 t3-topic-filtering/client.py <port> <PUBLISHER|SUBSCRIBER>
```
- Select or create a topic when prompted.


## Requirements
- Python 3.7 or higher
- No external dependencies (standard library only)
