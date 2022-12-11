#server
import socket, json
from Directory import Directory

class Server:
    def __init__(self, host:str, port:int):
        self.directory = Directory()

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind( (host, port) )

    @property
    def active_users(self):
        # Returns the list of handles of clients connected to the server
        return self.directory.handles

    @property
    def active_addresses(self):
        # Returns the list of client addresses connected to the server
        return self.directory.addresses


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
                self.directory.remove_client(address=client_address)
                self.send_response("Connection closed. Thank you!", client_address)


            elif command == 'register':
                handle = payload['handle']

                if handle in self.active_users:
                    self.send_response("Error: Registration failed. Handle or alias already exists.", client_address)
                else:
                    self.directory.add_client(client_address, handle)
                    self.send_response(f"Welcome {handle}!", client_address)


            elif command == 'all':
                client_handle = self.directory.get_handle(client_address)

                if client_handle in self.active_users:
                    message = payload['message']

                    for address in self.active_addresses:
                        self.send_response(f"{client_handle}: {message}", address)
                else:
                    self.send_response("Error: Handle or alias not found ", client_address)


            elif command == 'msg':
                sender_handle       = self.directory.get_handle(client_address)
                sender_address      = client_address

                if sender_handle in self.active_users:
                    receiver_handle     = payload['handle']
                    receiver_address    = self.directory.get_address(receiver_handle)
                    message             = payload['message']

                    if receiver_handle in self.active_users:
                        self.send_response(f'[To {receiver_handle}]: {message}', sender_address)
                        self.send_response(f'[From {sender_handle}]: {message}', receiver_address)
                    else:
                        self.send_response("Error: Handle or alias not found", sender_address)
                else:
                    self.send_response("Error: Handle or alias not found ", client_address)  


if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    try:
        server = Server(HOST, PORT)
        server.start()
    except:
        print('\nClosing server...')