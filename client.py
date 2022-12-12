import socket, json, time
from multiprocessing import Process
from tkinter import *
from threading import *


class Client:
    def __init__(self, master):
        self.handle = None
        self.socket = None
        self.server_address_port = None
        self.handle = None

        # thread for server responses
        self.t = None
        self.is_active_thread = False
        self.connected = False
        
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
        try:
            while self.is_active_thread:
                encoded_message, *_ = self.socket.recvfrom(1024)
                response = json.loads(encoded_message.decode('ascii'))

                if "prefix" in response and "type" in response:
                    if response["type"] == "CONFIRM_CONNECTION":
                        self.connected = True

                    elif response["type"] == "CLOSE_CONNECTION":
                        self.connected = False

                    elif response["type"] == "CONFIRM_HANDLE":
                        self.register(response['prefix'])

                    elif response["type"] == "RECEIVED_MESSAGE":
                        self.gui_print(text=response['prefix'], style="receiver", linebreak=False)

                    elif response["type"] == "SENT_MESSAGE":
                        self.gui_print(text=response['prefix'], style="sender", linebreak=False)

                    elif response["type"] == "BROADCAST_MESSAGE":
                        self.gui_print(text=response['prefix'], style="broadcast", linebreak=False)
                
                    self.gui_print(response['message'])

                elif "type" in response:
                    if response["type"] == "ERROR":
                        self.gui_print(text=response['message'], style='error')
                        

                else:
                    self.gui_print(response['message'])
        except:
            pass

    def connect(self, socket_address):
        # Connect to server
        self.server_address_port = socket_address
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        self.is_active_thread = True
        self.t = Thread(target=self.listen)
        self.t.start()

    def disconnect(self):
        # Disconnect from server
        self.connected = False
        self.is_active_thread = False
        #self.t.join()
        self.t = None
        
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
        
        # auto scroll to bottom
        self.chatwindow.see(END)

    def show_error(self, errorMessage):
        self.gui_print(text=errorMessage, style="error")

    def exec(self, evt=None):
        user_input = self.messageWindow.get("1.0",'end-1c')

        if user_input.strip():  # check if input box is blank
            command, *params = user_input.split()

            # reset input field
            self.messageWindow.delete(1.0, END)

            if command == '/join':
                # Connect to the server application
                # Syntax: /join <server_ip_add> <port>
                try:
                    server_ip_add, port = params
                    
                    if not self.connected:
                        try:
                            self.connect( (server_ip_add, int(port)) )
                            self.send({"command": "join"})

                            time.sleep(2)
                            if not self.connected:
                                raise Exception()

                        except Exception as e:
                            print(e)
                            self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                except:
                    self.show_error("Error: Command parameters do not match or is not allowed.")


            elif command == '/leave':
                # Disconnect to the server application
                if len(params) == 0:
                    if self.connected:
                        self.send({"command": "leave"})

                        time.sleep(2)
                        if not self.connected:
                            self.disconnect()
                    else:
                        self.show_error("Error: Disconnection failed. Please connect to the server first.")
                else:
                    self.show_error("Error: Command parameters do not match or is not allowed.")

            elif command == '/register':
                # Register a unique handle or alias
                # Syntax: /register <handle>
                try:
                    [handle] = params

                    if self.handle == None:
                        try:
                            self.send({"command": "register", "handle": handle})
                        except:
                            self.show_error("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
                    else:
                        self.show_error("Error: You have already registered.")
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
                self.gui_print("******** Commands for references ********\n" + \
                "\t /join <server_ip_add> <port>\n" + \
                "\t /leave \n" + \
                "\t /register <handle> \n" + \
                "\t /all <message> \n" + \
                "\t /msg <handle> <message> """)

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