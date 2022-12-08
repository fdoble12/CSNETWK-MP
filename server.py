#server
import socket, json

class Server:
    def __init__(self, host:str, port:int):
        self.directory = {}     # directory of clients. key = handle, value = client address

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind( (host, port) )

    @property
    def active_users(self):
        # Returns the list of handles of clients connected to the server
        return self.directory.keys()

    def get_handle(self, client_address):
        # Returns the client's handle given their address
        for handle, address in self.directory.items():
            if address == client_address:
                return handle

    def get_address(self, handle):
        # Returns the client's address given their handle
        return self.directory[handle]


    def send_response(self, response, client_address):
        # Send message to client (JSON)
        server_message = json.dumps( {"message": response} ).encode('ascii')
        self.socket.sendto(server_message, client_address)


    def start(self):
        print(f"Server listening to {self.host} {self.port}...")
       
        while True:
            # Listen for client requests
            client_message, client_address = self.socket.recvfrom(1024)
            payload = json.loads(client_message.decode())
            
            print(f"client #{client_address}: \t{payload}") # DEBUG: to check if narreceive ba talaga

            command = payload['command']
            if command == 'join':
                self.send_response("Connection to Message Board Server is successful!", client_address)


            elif command == 'leave':
                self.directory.pop(client_address)  # Remove client from active users
                self.send_response("Connection closed. Thank you!", client_address)


            elif command == '/register':
                handle = payload['handle']

                if handle in self.active_users:
                    self.send_response("Error: Registration failed. Handle or alias already exists.", client_address)
                else:
                    self.directory[handle] = client_address
                    self.send_response(f"Welcome {handle}!", client_address)


            elif command == '/all':
                client_handle = self.get_handle(client_address)

                if client_handle in self.active_users:
                    message = payload['message']

                    for address in self.active_users:
                        self.send_response(message, address)
                else:
                    self.send_response("Error: ", address)  # TODO: Add error message for unregistered users. Wala sa specs?


            elif command == '/msg':
                pass # TODO


if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    server = Server(HOST, PORT)
    server.start()