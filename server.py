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


    def send_response(self, response, client_address):
        server_message = json.dumps( {"message": response} ).encode('ascii')
        self.socket.sendto(server_message, client_address)


    def start(self):
        print(f"Server listening to {self.host} {self.port}...")
       
        while True:
            # Listen for client requests
            message, client_address = self.socket.recvfrom(1024)
            payload = json.loads(message.decode())
            
            print(f"client #{client_address}: \t{payload}") # DEBUG: to check if narreceive ba talaga

            command = payload['command']
            if command == 'join':
                self.send_response("Connection to Message Board Server is successful!", client_address)

            elif command == 'leave':
                self.send_response("Connection closed. Thank you!", client_address)

            elif command == '/register':
                handle = payload['handle']

                if handle in self.active_users:
                    self.send_response("Error: Registration failed. Handle or alias already exists.", client_address)
                else:
                    self.directory[handle] = client_address
                    self.send_response(f"Welcome {handle}!", client_address)

            elif command == '/all':
                pass    # TODO

            elif command == '/msg':
                pass    # TODO


if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    server = Server(HOST, PORT)
    server.start()