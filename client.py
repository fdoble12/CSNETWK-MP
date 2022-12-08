import socket, json

class Client:
    def __init__(self):
        self.handle = None
        self.socket = None
        self.server_address_port = None
    
    def send(self, message):
        # Send message to server
        client_message = json.dumps(message)   # convert message to JSON
        self.socket.sendto(client_message.encode(), self.server_address_port)

        #server_message, *_ = self.socket.recvfrom(1024)
        #return server_message.decode()

    def server_message(self):
        return self.socket.recv(1024).decode('ascii')

    def connect(self, socket_address):
        # Connect to server
        self.server_address_port = socket_address
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def disconnect(self):
        # Disconnect from server
        self.socket.close()

    def register(self, handle):
        # Registers user's handle. Assumes the handle is unique. Check with server first before calling this function.
        self.handle = handle



if __name__ == "__main__":
    client = Client()

    print("***** Welcome to  Message Board System *****")
    print("\ntype \"/?\" for the commands")

    while True:
        
        user_input = input('\n>> ')
        command, *params = user_input.split()
        

        if command == '/join':
            # Connect to the server application
            # Syntax: /join <server_ip_add> <port>
            try:
                server_ip_add, port = params
                
                try:
                    client.connect( (server_ip_add, int(port)) )
                    client.send({"command": "join"})
                    response = json.loads(client.server_message())
                    print(response['message']) #response from server
                except Exception as e:
                    print(e)
                    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            except:
                print("Error: Command parameters do not match or is not allowed.")


        elif command == '/leave':
            # Disconnect to the server application
            try:
                client.send({"command": "leave"})
                client.disconnect()
                print('Connection closed. Thank you!')
            except:
                print("Error: Disconnection failed. Please connect to the server first.")


        elif command == '/register':
            # Register a unique handle or alias
            # Syntax: /register <handle>
            try:
                [handle] = params

                try:
                    client.send({"command": "register", "handle": handle})
                    print ("Welcome, " + handle + "!")
                except:
                    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            except:
                print("Error: Command parameters do not match or is not allowed.")


        elif command == '/all':
            # Send message to all
            # Syntax: /all <message>
            message = ' '.join(params)

            try:
                client.send({"command": "all", "message": message})
                print("Sent to all: " + message)
            except:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")


        elif command == '/msg':
            # Send direct message to a single handle
            # Syntax: /msg <handle> <message>
            try:
                handle = params[0]
                message = ' '.join(params[1:])

                try:
                    client.send({"command": "msg", "handle": handle, "message": message})
                    print("[To " + handle + "]: " + message)
                except:
                    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

            except:
                print("Error: Command parameters do not match or is not allowed.")


        elif command == '/?':
            # Request command help to output all Input, Syntax commands for references
            print("\n*************************** Commands for references ***************************")
            print("/join <server_ip_add> <port>" + "\t\t" +       "Connect to the server application ")
            print("/leave"                       + "\t\t\t\t\t" + "Disconnect to the server application")
            print("/register <handle>"           + "\t\t\t" +     "Register a unique handle or alias")
            print("/all <message>"               + "\t\t\t\t" +   "Send message to all")
            print("/msg <handle> <message>"      + "\t\t\t" +     "Send direct message to a single handle\n\n")

        else:
            print("Error: Command not found.")