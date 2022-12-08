#server
import socket, json

class Server:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind( (host, port) )

    def listen(self):
        message, client_ip = self.socket.recvfrom(1024)

        # DEBUG: to check if narreceive ba talaga
        print(f'Got a connection from {client_ip}:')
        payload = json.loads(message.decode())
        print("Client Command: "+payload['command'])
        print(payload)
        print()

    def start(self):
        print(f"Server listening to {self.host} {self.port}...")
        while True:
            self.listen()

if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    server = Server(HOST, PORT)
    server.start()