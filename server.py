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
        payload = json.loads(message.decode())
        self.respond(payload, client_ip)
       

        # DEBUG: to check if narreceive ba talaga
        print(f'Got a connection from {client_ip}:')
        print("Client Command: "+payload['command'])
        print(payload)
        print()        

    def start(self):
        print(f"Server listening to {self.host} {self.port}...")
        while True:
            self.listen()

    def respond(self, payload, client_address):
        response = {"message":""}
        command = payload['command']
        if command == "join":
            response['message'] = "Connection to Mssage Board Server is successful!"
            self.socket.sendto(json.dumps(response).encode('ascii'), client_address)
        elif command == "leave":
            response['message'] = "Connection closed. Thank you!"
            self.socket.sendto(json.dumps(response).encode('ascii'), client_address)
            
if __name__ == "__main__":
    HOST    = socket.gethostname()
    PORT    = 8080

    server = Server(HOST, PORT)
    server.start()