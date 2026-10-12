import threading
import socket

host = '127.0.0.1'  # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message)
        except OSError:
            pass


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise ConnectionError
            broadcast(message)
        except (OSError, ConnectionError):
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames.pop(index)
                client.close()
                broadcast(f'{nickname} bro left the chat!'.encode('ascii'))
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('DORASIZEV'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        nicknames.append(nickname)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        threadn = threading.Thread(target=handle, args=(client,))
        threadn.start()


print("Server is listening...")
receive()