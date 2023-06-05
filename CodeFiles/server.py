import socket
from _thread import *
import filesystem as fs
from filesystem import clientInfo

#creating TCP Socket
#sock = socket.socket(socket.AF_NET, socket.SOCK_STREAM)


#get host name on which the server is being executed.
#host = socket.gethostname()
host = 'localhost'

#gets the IP address using the host name
print("The server IP address is: " socket.gethostbyname(host))
port = 95

#bind the socket
#server_address = (socket.gethostbyname(host), port)
#sock.bind(server_address)


ThreadCount = 0

usernames = ['admin']


def client_handler(connection):

    while True:
        data = connection.recv(2048)
        username = data.decode('utf-8')
        print('Please enter your Username :  ' + username)
        if username not in usernames:
            break
        connection.send(str.encode('Username is taken'))

    usernames.append(username)
    print(username + ' is sucessfully connected!')
    connection.send(str.encode(username + ' is sucessfully connected!'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        fs.thread_function(message)
        print(f"{username} ==> {clientInfo['message']}")
        if message == 'EXIT':
            print(username + ' is disconnected :(!')
            break
        reply = f"{username} ==> {clientInfo['message']}"
        connection.sendall(str.encode(reply))
    usernames.remove(username)
    connection.close()


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to socket ==> ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))


def start_server(host, port):
    #AF_INET specifies that the internet address is IPv4.
    #SOCK_STREAM specifies that the socket is TCP.
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ServerSocket.bind((socket.gethostbyname(host), port))
    except socket.error as e:
        print(str(e))
    print(f'\n ----Server is listening on the port {port}-----')
    #limiting the maximum nmuber of client connections to 5.
    ServerSocket.listen(5)

    while True:
        accept_connections(ServerSocket)


start_server(host, port)
