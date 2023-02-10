import socket               # sockets for connection
import threading            # threading for listening
from tkinter import *       # tkinter for GUI
from tkinter import font    #
from tkinter import ttk     #
 


PORT = 8080                 # set port for server connection

#Put in the public ip address of the host here
SERVER = "127.0.0.1"     # static server ip address

ADDRESS = (SERVER, PORT)   # set address for server as tuple

BYTES = 1024                # size of messages in bytes
FORMAT = "utf-8"            # encoding format
 


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create client socket
client.connect(ADDRESS)
 


# hex codes for colors
background = "#000000"
background_alt = "#121212"
foreground = "#ffffff"
foreground_i = "#00ff00"
 


# GUI class for the client
class GUI:



    # constructor method
    def __init__(self):
 
        self.Window = Tk()                  # create chat window
        self.Window.withdraw()              # hide it until after login
        
        self.login = Toplevel()             # create login window over chat window
        self.login.title("Login")           # set title
        self.login.resizable(width=False,   # make login static sized
                            height=False)
        self.login.configure(width=500,     # set login size
                            height=400,
                            bg=background)

        self.prompt = Label(self.login,                        # create prompt Label
                        bg=background,
                        fg=foreground,
                        text="Please login to continue",
                        justify=CENTER,
                        font="Consolas 14 bold")
        self.prompt.place(relheight=0.15,                      # set location of prompt
                        relx=0.25,
                        rely=0.07)

        self.nameLabel = Label(self.login,          # create "name:" label
                            bg=background,
                            fg=foreground,
                            text="Name: ",
                            font="Consolas 12")
        self.nameLabel.place(relheight=0.2,         # set location of label
                            relx=0.15,
                            rely=0.25)
 
        self.nameEntry = Entry(self.login,          # create entry for user input
                            bg=background_alt,
                            fg=foreground_i,
                            font="Consolas 14")
        self.nameEntry.place(relwidth=0.4,          # place location of entry
                            relheight=0.12,
                            relx=0.4,
                            rely=0.25)
        self.nameEntry.focus()  # set cursor focus to name entry
 
        # create login button
        self.start = Button(self.login,
                        bg=background_alt,
                        fg=foreground,
                         text="CONTINUE",
                         font="Consolas 14 bold",
                         command=lambda: self.goAhead(self.nameEntry.get()))
 
        self.start.place(relx=0.4,     # place login button
                      rely=0.6)

        self.Window.mainloop()      # run the event loop
 


    # move to chat window and start recv messages
    def goAhead(self, name):
        if name.strip() != '':
            self.login.destroy()        # destroy login screen
            self.layout(name)           # create layout for the chat (brings chat to front)
    
            # the thread to receive messages
            rcv = threading.Thread(target=self.receive)     # create thread
            rcv.start()                                     # start thread
 


    # layout of chat
    def layout(self, name):

        self.name = name                # set username of client

        self.Window.deiconify()                         # show chat window on call
        self.Window.title("Chatroom")                   # Set title
        self.Window.resizable(width=False,              # make chatroom static size
                              height=False)
        self.Window.configure(width=500,                # set size of chatroom
                              height=750,
                              bg=background_alt)

        self.headLabel = Label(self.Window,             # create header with client name
                               bg=background_alt,
                               fg=foreground,
                               text=self.name,
                               font="Consolas 13 bold",
                               pady=5)
        self.headLabel.place(relwidth=1)                # set location of header

        self.line = Label(self.Window,                  # create band at top of window
                          width=450,
                          bg=background_alt)
        self.line.place(relwidth=1,                     # set location
                        rely=0.07,
                        relheight=0.012)
 
        self.chatBox = Text(self.Window,                # create chat box
                             width=20,
                             height=2,
                             bg=background,
                             fg=foreground_i,
                             font="Consolas 14",
                             padx=5,
                             pady=5)
        self.chatBox.place(relheight=0.745,            # Place conversation box
                            relwidth=1,
                            rely=0.08)
 
        self.bottomLabel = Label(self.Window,           # create footer
                                 bg=background_alt,
                                 height=80)
        self.bottomLabel.place(relwidth=1,              # place footer
                               rely=0.825)
 
        self.messageEntry = Entry(self.bottomLabel,                 # create message entry
                              bg=background_alt,
                              fg=foreground_i,
                              insertbackground=foreground_i,
                              font="Consolas 13")
        self.messageEntry.place(relwidth=0.74,                      # set place entry
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)
        self.messageEntry.focus()                                   # set focus on text entry
 
        self.messageButton = Button(self.bottomLabel,               # create Send Button
                                text="Send",
                                font="Consolas 10 bold",
                                width=20,
                                bg=background,
                                fg=foreground,
                                command=lambda: self.buttonClick(self.messageEntry.get()))
        self.Window.bind('<Return>', lambda event: self.buttonClick(self.messageEntry.get()))
        self.messageButton.place(relx=0.77,                         # palce button
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)
 
        self.chatBox.config(cursor="arrow")                    # set cursor over chat
        scrollbar = Scrollbar(self.chatBox)                    # create scroll bar for chat
        scrollbar.place(relheight=1,                            # place scroll bar
                        relx=0.974)
        scrollbar.config(command=self.chatBox.yview)           # set which way window scrolls
        self.chatBox.config(state=DISABLED)                    # set text to not be edited
        
 

    # function to basically start the thread for sending messages
    def buttonClick(self, msg):
        print("Sending message...")
        self.chatBox.config(state=DISABLED)    # when sending message disable chat print
        self.message = msg                          # set self.message to message
        self.messageEntry.delete(0, END)

        snd = threading.Thread(target=self.send)     # create thread 
        snd.start()                                         # start thread

 

    # receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(BYTES).decode(FORMAT)     # recieve message from server
 
                # if message from server is NAME send self.name for C/S setup
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))       # send name to server
                else:
                    # insert messages to chat
                    self.chatBox.config(state=NORMAL)      # allow text to be added
                    self.chatBox.insert(END,               # insert text to window after last message
                                         message+"\n\n")
 
                    self.chatBox.config(state=DISABLED)    # remove add text
                    self.chatBox.see(END)                  # make sure text scrolls to show new messages
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                client.close()
                break
 


    # send messages
    def send(self):
        self.chatBox.config(state=DISABLED)            # disable text insert while sending message
        while True:
            if self.message.strip() != '':
                message = (f"{self.name} >> {self.message}")    # format string for send to other users
                client.send(message.encode(FORMAT))         # send created message to client for disperse
            break                                       # break after sending message
 
 

# create GUI
g = GUI()