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
        server_message = ""
        if isinstance(response, str):
            server_message = json.dumps( {"message": response} ).encode('ascii')
        elif isinstance(response, object):
            server_message = json.dumps( response ).encode('ascii')
        self.socket.sendto(server_message, client_address)

    def send_error(self, errorMsg, client_address):
        error_response = {
            "message": errorMsg,
            "type": "ERROR"
        }
        self.send_response(error_response, client_address)

    def start(self):
        print(f"Server listening to {self.host} {self.port}...")
       
        while True:
            # Listen for client requests
            client_message, client_address = self.socket.recvfrom(1024)
            payload = json.loads(client_message.decode())
            
            print(f"client #{client_address}: \t{payload}") # DEBUG: to check if narreceive ba talaga

            command = payload['command']

            if command == 'join':
                confirmation_response = {
                    "message": "Connection to Message Board Server is successful!",
                    "type": "CONFIRM_CONNECTION",
                    "prefix": ""
                }
                self.send_response(confirmation_response, client_address)


            elif command == 'leave':
                disconnect_response = {
                    "message": "Connection closed. Thank you!",
                    "type": "CLOSE_CONNECTION",
                    "prefix": ""
                }
                self.send_response(disconnect_response, client_address)
                self.directory.remove_client(address=client_address)


            elif command == 'register':
                handle = payload['handle']

                if handle in self.active_users:
                    self.send_error("Error: Registration failed. Handle or alias already exists.", client_address)
                else:
                    self.directory.add_client(client_address, handle)

                    welcome_response = {
                        "message": f"Welcome {handle}!",
                        "type": "CONFIRM_HANDLE",
                        "prefix": handle
                    }
                    self.send_response(welcome_response, client_address)


            elif command == 'all':
                client_handle = self.directory.get_handle(client_address)

                if client_handle in self.active_users:
                    message = payload['message']

                    for address in self.active_addresses:
                        broadcast_response = {
                            "message": message,
                            "prefix": f'{client_handle}: ',
                            "type": "BROADCAST_MESSAGE"
                        }
                        self.send_response(broadcast_response, address)
                else:
                    self.send_error("Error: Handle or alias not found ", client_address)


            elif command == 'msg':
                sender_handle       = self.directory.get_handle(client_address)
                sender_address      = client_address

                if sender_handle in self.active_users:
                    receiver_handle     = payload['handle']
                    receiver_address    = self.directory.get_address(receiver_handle)
                    message             = payload['message']

                    if receiver_handle in self.active_users:
                        sender_response = {
                            "message": message,
                            "prefix": f'[To {receiver_handle}]: ',
                            "type": "SENT_MESSAGE"
                        }
                        self.send_response(sender_response, sender_address)

                        receiver_response = {
                            "message": message,
                            "prefix": f'[From {sender_handle}]: ',
                            "type": "RECEIVED_MESSAGE"
                        }
                        self.send_response(receiver_response, receiver_address)
                    else:
                        self.send_error("Error: Handle or alias not found", sender_address)
                else:
                    self.send_error("Error: Handle or alias not found ", client_address)  


if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    try:
        server = Server(HOST, PORT)
        server.start()
    except:
        print('\nClosing server...')