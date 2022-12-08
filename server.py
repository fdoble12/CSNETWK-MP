#server
import socket
import json


def start_server():
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST,PORT))
        print("Server listeng to "+HOST+" "+str(PORT)+"...")
    except:
        print("Error binding server...")
    
    server_socket.listen(1)
    
    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print("Got a connection from %s" % str(addr))
        client_command = json.loads(client_socket.recv(1024).decode('ascii'))
        print("Client Command: "+client_command['command'])
        
        if client_command['command'] == "join":
            client_socket.send("Connection to Message Board Server is succesful!".encode('ascii'))
        
        
if __name__ == "__main__":
    start_server()
