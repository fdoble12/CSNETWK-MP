import socket, json
from multiprocessing import Process
from tkinter import *
from threading import *


class Client:
    def __init__(self, master):
        self.handle = None
        self.socket = None
        self.server_address_port = None

        # thread for server responses
        self.t = Thread(target=self.listen)
        self.activeThread = False
        
        # GUI
        self.root = master
        self.create_gui()

        self.gui_print("***** Welcome to  Message Board System *****")
        self.gui_print("type \"/?\" for the commands")
    
    def send(self, message):
        # Send message to server
        client_message = json.dumps(message)   # convert message to JSON
        self.socket.sendto(client_message.encode(), self.server_address_port)
        
    def server_message(self):
        return self.socket.recv(1024).decode('ascii')

    def listen(self):
        while True:
            encoded_message, *_ = self.socket.recvfrom(1024)
            response = json.loads(encoded_message.decode('ascii'))

            if "prefix" in response and "type" in response:
                if response["type"] == "RECEIVED_MESSAGE":
                    self.gui_print(text=response['prefix'], style="receiver", linebreak=False)

                elif response["type"] == "SENT_MESSAGE":
                    self.gui_print(text=response['prefix'], style="sender", linebreak=False)

                elif response["type"] == "BROADCAST_MESSAGE":
                    self.gui_print(text=response['prefix'], style="broadcast", linebreak=False)

            self.gui_print(response['message'])

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
        self.head_label = Label(root, bg="white", text=" Welcome to Message Board System ",  font=("Arial", 13), pady=10)
        self.head_label.place(relwidth=1)

        #create chat window
        self.chatwindow = Text(root, bg= "beige", width= 50, height= 8)
        self.chatwindow.place(x= 15, y= 50, height= 330, width= 370)

        #create message area
        self.messageWindow = Text(root, bd= 3, bg= "beige", width= 30, height= 4)
        self.messageWindow.place (x= 15, y= 400, height= 88, width= 260)

        #button for sending
        self.button = Button(root, text = "Enter", bg= "white", activebackground = "light blue", font=("Arial", 13), width = 5, height = 5, command=self.exec)
        self.button.place(x= 285, y= 400, height= 88, width= 100)

        #scroll bar
        self.scroll = Scrollbar(root, command=self.chatwindow.yview())
        self.scroll.place(x= 375, y=50, height= 330)

        #listen to enter key for commands
        self.root.bind('<Return>', self.exec)

        # self.win.protocol("WM_DELETE_WINDOW", self.stop)

    def gui_print(self, text='', style='', linebreak=True):
        # existing styles
        self.chatwindow.tag_config('sender', foreground="blue")
        self.chatwindow.tag_config('receiver', foreground="red")
        self.chatwindow.tag_config('broadcast', foreground="green")
        self.chatwindow.tag_config('error', foreground="red")

        if style == '':
            self.chatwindow.insert(END, text + ('\n\n' if linebreak else ''))
        else:
            self.chatwindow.insert(END, text + ('\n\n' if linebreak else ''), style)

    def show_error(self, errorMessage):
        self.gui_print(text=errorMessage, style="error")

    def exec(self, evt=None):
        user_input = self.messageWindow.get("1.0",'end-1c')

        if user_input.strip():  # check if input box is blank
            command, *params = user_input.strip().split()

            # reset input field
            self.messageWindow.delete(1.0, END)

            if command == '/join':
                # Connect to the server application
                # Syntax: /join <server_ip_add> <port>
                try:
                    server_ip_add, port = params
                    
                    try:
                        self.connect( (server_ip_add, int(port)) )
                        self.send({"command": "join"})

                        if not self.activeThread:
                            self.t.start()
                            self.activeThread = True
                    except:
                        self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                except:
                    self.show_error("Error: Command parameters do not match or is not allowed.")


            elif command == '/leave':
                # Disconnect to the server application
                try:
                    self.send({"command": "leave"})
                    self.disconnect()
                except:
                    self.show_error("Error: Disconnection failed. Please connect to the server first.")


            elif command == '/register':
                # Register a unique handle or alias
                # Syntax: /register <handle>
                try:
                    [handle] = params

                    try:
                        self.send({"command": "register", "handle": handle})
                    except:
                        self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                except:
                    self.show_error("Error: Command parameters do not match or is not allowed.")


            elif command == '/all':
                # Send message to all
                # Syntax: /all <message>
                message = ' '.join(params)

                try:
                    self.send({"command": "all", "message": message})
                except:
                    self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")


            elif command == '/msg':
                # Send direct message to a single handle
                # Syntax: /msg <handle> <message>
                try:
                    handle = params[0]
                    message = ' '.join(params[1:])

                    try:
                        self.send({"command": "msg", "handle": handle, "message": message})
                    except:
                        self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

                except:
                    self.show_error("Error: Command parameters do not match or is not allowed.")


            elif command == '/?':
                # Request command help to output all Input, Syntax commands for references
                self.gui_print("************* Commands for references *************\n" + \
                "/join <server_ip_add> <port>    Connect to the server application\n" + \
                "/leave                          Disconnect to the server application\n" + \
                "/register <handle>              Register a unique handle or alias\n" + \
                "/all <message>                  Send message to all\n" + \
                "/msg <handle> <message>         Send direct message to a single handle\n""")

            else:
                self.show_error("Error: Command not found.")



if __name__ == "__main__":
    root = Tk()
    client = Client(root)

    root.send

    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Disconnect client before exiting program
        if client.socket != None:
            client.send({"command": "leave"})
            client.disconnect()