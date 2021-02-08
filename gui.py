import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

class GUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("end-to-end Discord")
        self.root.geometry("1024x720")
        self.root.configure(background="white")

        self.loginPage = tk.Frame(self.root, bg="white")
        self.mainPage = tk.Frame(self.root, bg="white")

        for frame in (self.loginPage, self.mainPage):
            frame.grid(row=10, column=10, sticky='nesw')

    def showPage(self, page):
        page.tkraise()

    def run(self):
        self.root.mainloop()

    def configure_loginPage(self):
        container = tk.Label(self.loginPage, bg="white", height=11)
        container.grid(row=0, column=0)

        loginLabel = tk.Label(self.loginPage, text="Input your Discord token" ,bg="white", \
                                width=45, height=2, anchor="w", pady=0)
        loginLabel['font'] = tkFont.Font(family = "Arial Narrow", size=40)
        loginLabel.grid(row=1, column=0, padx=70, pady=0)

        self.tokenEntry = tk.Entry(self.loginPage, width=30, bd=2, \
                                        relief="flat", highlightbackground="#b9c4f1", \
                                        highlightthickness=2)
        self.tokenEntry.config(highlightbackground="black", highlightcolor="black", border=4)
        self.tokenEntry['font'] = tkFont.Font(family="Arial", size=35)
        self.tokenEntry.grid(row=2, column=0, sticky="w", padx=70, pady=0)

        buttonStartingPage = tk.Button(self.loginPage, bg="black",anchor="center", fg="white",bd=0, \
                                        height=2, activebackground="white", text="Login", \
                                        width=10, command=self.collect_dcToken)
        buttonStartingPage['font'] = tkFont.Font(family="Arial", size=12, weight="bold")
        buttonStartingPage.grid(row=3, column=0, pady=50, padx=70, sticky = "w")

    def collect_dcToken(self):
        token = self.tokenEntry.get()
        print(f"Collected token: {token}")
        #TODO login with the discord bot
        self.configure_mainPage()
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

        # pole 
        self.chatEntry = tk.Entry(left_frame, bd=2, bg="white", width=26, relief="flat", selectborderwidth=2, highlightthickness=2)
        self.chatEntry.config(highlightbackground="black", highlightcolor="black")
        self.chatEntry['font'] = tkFont.Font(family="Arial", size=26)
        self.chatEntry.place(x=50, y=640)

        #przycik wyslij w narzedzia
        PrzyciskNarzedziaWyslij = tk.Button(left_frame, text="Send", fg="white", bg="black", width=10,\
                                            relief="solid", height=2, anchor="center", \
                                            activebackground="white", activeforeground="black",\
                                            command=lambda: self.send_msg())
        PrzyciskNarzedziaWyslij['font'] = tkFont.Font(family="Arial", size=12, weight="bold")
        PrzyciskNarzedziaWyslij.place(x=580, y=640)
        ############################################################################################

        # szara strefa
        ############################################################################################

        textSzaraStrefa = tk.Text(right_frame, bg="#D3D3D3",yscrollcommand=1, exportselection=1, \
                                    bd=0, height=21,selectbackground="#B1B1B1", width=18, \
                                    state="disabled", highlightbackground="#D3D3D3")
        textSzaraStrefa['font'] = tkFont.Font(family="Arial", size=20)
        textSzaraStrefa.place(x=10, y=10)

    def send_msg(self):
        msg = self.chatEntry.get()
        print(msg)
        self.chatEntry.delete(0, len(msg) )


if __name__ == "__main__":
    window = GUI()
    window.configure_loginPage()
    window.showPage(window.loginPage)
    window.run()

