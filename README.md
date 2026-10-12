# Multi-Client Chat Room with Python Sockets

A terminal-based chat application that lets multiple users exchange messages in real time. 
A single server accepts many client connections and broadcasts every message to all connected clients. 
Built using only the Python standard library (`socket` and `threading`).

## Features

- Multiple clients can connect to one server at the same time
- Nickname selection when joining
- Messages from one client are broadcast to all clients
- Notifications when users join and leave the chat
- No external dependencies

## Tech Stack

| Component | Purpose |
|---|---|
| `socket` (`AF_INET`, `SOCK_STREAM`) | TCP connection between server and clients |
| `threading` | One thread per client on the server; separate receive and send threads on the client |
| `127.0.0.1:55555` | Server address and port (localhost) |

## Project Structure

```
.
├── server.py   # Server: accepts connections and broadcasts messages
├── client.py   # Client: sends and receives messages
└── README.md
```

## Requirements

- Python 3.8 or newer

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/<username>/<repository-name>.git
   cd <repository-name>
   ```

2. Start the server in one terminal:

   ```bash
   python server.py
   ```

   The server prints `Server is listening...`.

3. Start a client in another terminal (repeat in several terminals to simulate multiple users):

   ```bash
   python client.py
   ```

4. Enter a nickname and start chatting. Your messages appear on every connected client.

## How It Works

### Architecture

```
 Client A  <──►  Server  <──►  Client B
                   ▲
                   └────────►  Client C
```

Each client is handled by its own thread on the server, so many users can be active at once.

### Connection and Nickname Flow

1. The client connects to the server over TCP.
2. The server sends the code `DORASIZEV` as a nickname request.
3. The client replies with its chosen nickname.
4. The server stores the client and its nickname, broadcasts a join message, and starts a `handle()` thread for that client.

### Main Server Functions

| Function | Role |
|---|---|
| `broadcast(message)` | Sends a message to every connected client |
| `handle(client)` | Receives messages from one client and forwards them via `broadcast()`; cleans up when the client disconnects |
| `receive()` | Accepts new connections, runs the nickname handshake, and starts a thread for each client |

### Main Client Functions

| Function | Role |
|---|---|
| `receive()` | Receives messages from the server and prints them; replies with the nickname when requested |
| `write()` | Reads user input and sends it to the server prefixed with the nickname |

## Configuration

The host and port are hard-coded:

```python
host = '127.0.0.1'
port = 55555
```

To run on a local network, change `host` in the server (for example to `0.0.0.0`) and the target address in the client to the server machine's IP.

## Known Limitations

- Messages are encoded as ASCII, so non-ASCII characters (such as emoji) are not supported yet
- No authentication or encryption; messages are sent as plain text

## License

This project is [MIT](LICENSE) licensed.