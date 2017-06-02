from Tkinter import *
# import ttk
import webbrowser
from authhelper import get_signin_url

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.open_button = Button(master, text="Open", command=self.openPage)
        self.open_button.pack()

    def greet(self):
        print("Greetings!")

    def openPage(self):
        webbrowser.open_new("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?scope=openid+User.Read+Mail.Read&response_type=code&client_id=c6e045c9-e53e-4009-9b39-80990ae99637")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()