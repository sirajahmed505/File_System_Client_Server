import socket
print("================================================================================")
print('                        WELCOME TO THE DISTRIBUTED FILE SYSTEM                  ')
print("================================================================================")
print("This remote file system supports the following commands;   \
      the command format is also specified with each command.\n")
print("1. Create a file: 'create file_name.txt'\n \
    2. Delete a file: 'delete file_name.txt'\n \
    3. Create a directory: '' mkdir dir_name'\n \
    4. Change the directory : 'changeDir dir_name'\n \
    5. Move a file: 'mov file_name.txt dir_name'\n \
    Note: The file modes are 'w' for write and 'r' for read.\n \
    6. Open a file: 'open <file_name.txt,mode>'\n \
    7. Close a file: 'close <file_name>'\n \
    8. Write to a file: 'write_to_file <file_name.txt>,string_to_write'\n \
    9. Read from a file: 'read_from_file <file_name.txt>,starting_position,end_position'\n \
    Note: to read whole file use starting_position as 0 and end_position as -1.\n \
    10. Truncate a file: 'truncate_file file_name.txt position'\n \
    11. Show memory Map: 'show'\n \
    12. To exit the system enter: 'BYE' (We'll be sorry to see you go :(\
    That's all folks, enjoy using the distributed file system! \n")
print("The client is ready to connect!\n")
while True:
    #host = input('Enter the IP address of the server:  ')
    host = 'localhost'
    port = 95

    #AF_INET specifies that the internet address is IPv4.
    #SOCK_STREAM specifies that the socket is TCP.
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ClientSocket.connect((host, port))
        print('Connection Successful!!')
        break
    except socket.error as e:
        print("The IP you have entered might be INCORRECT OR Server NOT running(It's not you, it's US.)")

while True:
    username = input("Please enter your Username :  ")
    ClientSocket.send(str.encode(username))
    Response = ClientSocket.recv(2048)
    if Response.decode('utf-8') != 'This username is taken :(':
        break
    print(Response.decode('utf-8'))

print(Response.decode('utf-8'))
while True:
    Input = input('Enter Command: ')
    if Input == 'EXIT':
        ClientSocket.send(str.encode(Input))
        break
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(2048)
    print(Response.decode('utf-8'))

ClientSocket.close()
print("Connection Terminated Successfully.")
