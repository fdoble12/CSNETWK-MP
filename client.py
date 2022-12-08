import socket
import json

class client:
    def __init__(self):
        self.client_socket = None
        
    def receive_message(self):
        data = self.client_socket.recv(1024).decode('ascii')
        print("Server sent: %s" % data)
        
    def connect_to_server(self,server_ip_add,port):
        # socket object
        print ("Connecting to Host: "+server_ip_add+" in Port: "+ port+"...")
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip_add, int(port)))
            jsonCommand = json.dumps({"command":"join"})
            self.client_socket.send(jsonCommand.encode('ascii')) 
        except:
            print("Can't connect to server...")
        
    
    def parse_input(self,input_string):
        command, *params = input_string.split()

        if command == '/join':
            # Connect to the server application
            # Syntax: /join <server_ip_add> <port>
            try:
                server_ip_add, port = params
                self.connect_to_server(server_ip_add,port)
            except:
                print("Error: Command parameters do not match or is not allowed.")

        elif command == 'leave':
            # Disconnect to the server application
            pass

        elif command == '/register':
            # Register a unique handle or alias
            # Syntax: /register <handle>
            try:
                [handle] = params
            except:
                print("Error: Command parameters do not match or is not allowed.")

        elif command == '/all':
            # Send message to all
            # Syntax: /all <message>
            message = ' '.join(params)

        elif command == '/msg':
            # Send direct message to a single handle
            # Syntax: /msg <handle> <message>
            try:
                handle = params[0]
                message = ' '.join(params[1:])
            except:
                print("Error: Command parameters do not match or is not allowed.")

        elif command == '/?':
            # Request command help to output all Input, Syntax commands for references
            pass

        else:
            print("Error: Command not found.")


if __name__ == "__main__":
    myClient = client()
    while True:
        user_input = input('>> ')
        myClient.parse_input(user_input)
        myClient.receive_message()