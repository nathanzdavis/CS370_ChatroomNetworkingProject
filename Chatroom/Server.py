import socket       # sockets for connection
import threading    # threading for listening

PORT = 8080                                             # set port for server

#uncomment the below line for p2p.  It will dynamically assign the host ip
#SERVER = socket.gethostbyname(socket.gethostname())  

#comment the line below out if you are using the above line
SERVER = "127.0.0.1"     # get ip address for server

ADDRESS = (SERVER, PORT)                                # set address for server as tuple

BYTES = 1024        # size of messages in bytes
FORMAT = "utf-8"    # encoding format



# lists of clients and usernames connected to server
clients = []
names = []



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # set socket for the server
server.bind(ADDRESS)                                        # bind the address to the socket



# broadcast to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)



# handle incoming messages
def handle(connection, address):

    # connection established True
    print(f"new connection {address}")
    connected = True

    while connected:
        # receive then broadcast
        message = connection.recv(BYTES)
        broadcast(message)

    # close connection
    connection.close()



# function to start the connection
def startServer():
    # pront server address to console
    print("server is working on " + SERVER + ":" + str(PORT))

    # listen for connections
    server.listen()


    while True:
        # connection to client, and its bound address
        connection, address = server.accept()
        connection.send("NAME".encode(FORMAT))

        # recieve username from client
        name = connection.recv(BYTES).decode(FORMAT)

        # append to appropriate lists
        names.append(name)
        clients.append(connection)

        print(f"User: {name}")

        # broadcast message
        broadcast(f"{name} has joined.".encode(FORMAT))

        connection.send('Connection successful.'.encode(FORMAT))

        # create thread to handle recv message from client
        thread = threading.Thread(target=handle, args=(connection, address))
        thread.start()

        # number of clients connected
        print(f"Connections: {threading.activeCount()-1}")



startServer()