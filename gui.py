import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from bot import start_bot, database 
import time, threading


class GUI(object):
    def __init__(self, DC_TOKEN=""):
        self.DC_TOKEN = DC_TOKEN
        self.root = tk.Tk()
        self.root.title("end-to-end Discord")
        self.root.geometry("1024x720")
        self.root.configure(background="white")

        self.loginPage = tk.Frame(self.root, bg="white")
        self.mainPage = tk.Frame(self.root, bg="white")

        for frame in (self.loginPage, self.mainPage):
            frame.grid(row=10, column=10, sticky='nesw')

        self.sync_thread = threading.Thread(target=self.sync)
        self.sync_thread.deamon = True
        self.sync_thread.start()

    def sync(self):
        previous_database = database
        print("Started sync")
        print(previous_database)
        print('-' * 30)
        while True:
            self.update_chats(database['chats'])
            time.sleep(1)

    def update_chats(self, chats):
        for key, val in chats.items():
            print(key, val)
            self.field.insert('1.0', f'{key}\n\n')

    def showPage(self, page):
        page.tkraise()

    def run(self):
        self.root.mainloop()

    def configure_loginPage(self):
        container = tk.Label(self.loginPage, bg="white", height=11)
        container.grid(row=0, column=0)

        loginLabel = tk.Label(self.loginPage, text="Input your Discord token" ,bg="white", \
                                width=45, height=2, anchor="w", pady=0)
        loginLabel['font'] = tkFont.Font(size=40)
        loginLabel.grid(row=1, column=0, padx=70, pady=0)

        self.tokenEntry = tk.Entry(self.loginPage, width=70, bd=2, \
                                        relief="flat", highlightbackground="#b9c4f1", \
                                        highlightthickness=2)
        self.tokenEntry.insert(0, self.DC_TOKEN)
        self.tokenEntry.config(highlightbackground="black", highlightcolor="black", border=4)
        self.tokenEntry['font'] = tkFont.Font(size=15)
        self.tokenEntry.grid(row=2, column=0, sticky="w", padx=70, pady=0)

        self.option = tk.IntVar(value=1)
        remember_checkbox = tk.Checkbutton(self.loginPage, text='Remember me', bg="white", relief="flat", variable=self.option, onvalue=1, offvalue=0)
        remember_checkbox['font'] = tkFont.Font(size=15)
        remember_checkbox.grid(row=3, column=0, sticky="w", padx=70, pady=20)

        loginButton = tk.Button(self.loginPage, bg="black",anchor="center", fg="white",bd=0, \
                                        height=2, activebackground="white", text="Login", \
                                        width=10, command=self.collect_dcToken)
        loginButton['font'] = tkFont.Font(size=12, weight="bold")
        loginButton.grid(row=4, column=0, pady=20, padx=70, sticky = "w")

    def collect_dcToken(self):
        token = self.tokenEntry.get()
        remember = self.option.get()

        print(f"Collected token: {token}")

        if remember == 1:
            with open("dcToken.txt", "w+") as f:
                f.write(token)

        #TODO login with the discord bot in a separate thread
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.deamon = True
        bot_thread.start()
        self.showPage(self.mainPage)

    def configure_mainPage(self):
        left_frame = tk.Frame(self.mainPage, width=704, height=720, bg="white")
        left_frame.grid(row=0, column=1)
        right_frame = tk.Frame(self.mainPage, width=290, height=720, bg="#D3D3D3")
        right_frame.grid(row=0, column=0)

        chatUsername = tk.Label(left_frame, text="Test_user", bg="white")
        chatUsername['font'] = tkFont.Font(family="Arial", size=17, weight="bold")
        chatUsername.place(x=50, y=0)

        chatHistory = tk.Text(left_frame, bg="#D3D3D3",yscrollcommand=1, exportselection=1, \
                                    bd=0, height=18,selectbackground="#B1B1B1", width=42, \
                                    state="disabled", highlightbackground="#D3D3D3")
        chatHistory['font'] = tkFont.Font(family="Arial", size=20)
        chatHistory.place(x=50, y=40)

        self.chatEntry = tk.Entry(left_frame, bd=2, bg="white", width=26, relief="flat", selectborderwidth=2, highlightthickness=2)
        self.chatEntry.config(highlightbackground="black", highlightcolor="black")
        self.chatEntry['font'] = tkFont.Font(family="Arial", size=26)
        self.chatEntry.place(x=50, y=640)

        sendMsgButton = tk.Button(left_frame, text="Send", fg="white", bg="black", width=10,\
                                            relief="solid", height=2, anchor="center", \
                                            activebackground="white", activeforeground="black",\
                                            command=lambda: self.send_msg())
        sendMsgButton['font'] = tkFont.Font(family="Arial", size=12, weight="bold")
        sendMsgButton.place(x=580, y=640)


        #TODO other chats will be shown here
        self.field = tk.Text(right_frame, bg="red",yscrollcommand=1, exportselection=1, \
                                    bd=0, height=21,selectbackground="#B1B1B1", width=18, \
                                    state="normal", highlightbackground="#D3D3D3")
        self.field['font'] = tkFont.Font(family="Arial", size=20)
        self.field.place(x=10, y=10)
        self.field.insert('1.0', 'siemka co tam')

    def send_msg(self):
        msg = self.chatEntry.get()
        print(msg)
        print(database)
        self.chatEntry.delete(0, len(msg) )


if __name__ == "__main__":
    #Check if the token is already stored in dcToken.txt
    try:
        with open("dcToken.txt", "r") as f:
            token = ''.join(f.readlines()) 
    except:
        print("Could not find a dcToken file")
    window = GUI(token)
    window.configure_loginPage()
    window.configure_mainPage()
    window.showPage(window.loginPage)
    window.run()

