import socket, json
from multiprocessing import Process
from tkinter import *


class Client:
    def __init__(self, master):
        self.handle = None
        self.socket = None
        self.server_address_port = None
        
        self.root = master
        self.create_gui()

    
    def send(self, message):
        # Send message to server
        client_message = json.dumps(message)   # convert message to JSON
        self.socket.sendto(client_message.encode(), self.server_address_port)
        

    def server_message(self):
        return self.socket.recv(1024).decode('ascii')

    def listen(self):
        while True:
            if self.socket:
                encoded_message, *_ = self.socket.recvfrom(1024)
                response = json.loads(encoded_message.decode('ascii'))
                print(response['message'] + '\n')

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

    #GUI PART
    def create_gui(self):
        self.root.title("Message Board System") 
        self.root.geometry('400x500')

        #header
        head_label = Label(root, bg="white", text=" Welcome to Message Board System ",  font=("Arial", 13), pady=10)
        head_label.place(relwidth=1)

        #create chat window
        chatwindow = Text(root, bg= "beige", width= 50, height= 8)
        chatwindow.place(x= 15, y= 50, height= 330, width= 370)

        #create message area
        messageWindow = Text(root, bd= 3, bg= "beige", width= 30, height= 4)
        messageWindow.place (x= 15, y= 400, height= 88, width= 260)

        #button for sending
        button = Button(root, text = "Enter", bg= "white", activebackground = "light blue", font=("Arial", 13), width = 5, height = 5)
        button.place(x= 285, y= 400, height= 88, width= 100)

        #scroll bar
        scroll = Scrollbar(root, command=chatwindow.yview())
        scroll.place(x= 375, y=50, height= 330)

        # self.win.protocol("WM_DELETE_WINDOW", self.stop)

    

if __name__ == "__main__":
    root = Tk()
    client = Client(root)
    proc = Process(target=client.listen)

    print("***** Welcome to  Message Board System *****")
    print("\ntype \"/?\" for the commands")

    root.send

    try:
        while True:
            user_input = input()
            command, *params = user_input.split()
            

            if command == '/join':
                # Connect to the server application
                # Syntax: /join <server_ip_add> <port>
                try:
                    server_ip_add, port = params
                    
                    try:
                        client.connect( (server_ip_add, int(port)) )
                        client.send({"command": "join"})
                        proc.start()
                    except:
                        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                except:
                    print("Error: Command parameters do not match or is not allowed.")


            elif command == '/leave':
                # Disconnect to the server application
                try:
                    client.send({"command": "leave"})
                    client.disconnect()
                except:
                    print("Error: Disconnection failed. Please connect to the server first.")


            elif command == '/register':
                # Register a unique handle or alias
                # Syntax: /register <handle>
                try:
                    [handle] = params

                    try:
                        client.send({"command": "register", "handle": handle})
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
                    except:
                        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

                except:
                    print("Error: Command parameters do not match or is not allowed.")


            elif command == '/?':
                # Request command help to output all Input, Syntax commands for references
                print("\n*************************** Commands for references ***************************")
                print("\t/join <server_ip_add> <port>")
                print("\t/leave")
                print("\t/register <handle>")
                print("\t/all <message>")
                print("\t/msg <handle> <message>")

            else:
                print("Error: Command not found.")

    except KeyboardInterrupt:
        # Disconnect client before exiting program
        if client.socket != None:
            client.send({"command": "leave"})
            client.disconnect()
            proc.terminate()