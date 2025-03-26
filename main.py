import tkinter as tk
from Frame1 import Frame1
from Frame2 import Frame2
from components import frames, colors
from mysql.connector import connection




class MyOptionButton(tk.Button):
    def __init__(self, parent, buttonText, backgroundColor, rowConfiguration, representingFrame, changeScreen):
        super().__init__( parent)
        self.changeScreen = changeScreen
        self.representingFrame = representingFrame
        self.configure(text=f"{buttonText}", bg=f"{backgroundColor}", height=4, command=self.changeFrame, foreground="white")
        self.grid(column=0, row=rowConfiguration, sticky="EW")
    def changeFrame(self):
        #print('changeing frame to ' + str(self.representingFrame))
        # app.changeScreen(frames["do przeczytania"])
        self.changeScreen(self.representingFrame)

class MenuFrame(tk.Frame):
    def __init__(self, parent, changeScreenFunction):
        super().__init__(parent)
        self.changeScreen = changeScreenFunction
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.titleLabel = tk.Label(self, text="BIBLIOTECZKA", fg=colors["brown"])
        self.titleLabel.grid(column=0, row=0)

        self.btn1 = MyOptionButton(self, "hello", colors["lightgreen"], 1, frames["do przeczytania"], self.changeScreen)

        self.btn2 = MyOptionButton(self, "world", colors["darkgreen"], 2, frames["w trakcie"], self.changeScreen)

        self.btn2 = MyOptionButton(self, "how are you", colors["brown"], 3, frames["skonczone"], self.changeScreen)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.grid(column=0, row=0, padx=25, pady=25, sticky="NSEW")




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bookcase")
        self.geometry("400x400")
        self.resizable(False, False)
        self.configure(background=colors["beige"])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.menuPage = MenuFrame(self, self.changeScreen)
        self.frame1 = Frame1(self, self.changeScreen)
        self.frame2 = Frame2(self, self.changeScreen)

    def changeScreen(self, frame):

        if frame == frames["menu"]:
            self.menuPage.tkraise()
            self.menuPage.grid(row=0, column=0)
            self.frame2.destroy()
        elif frame == frames["do przeczytania"]:
            self.frame1.grid(row=0, column=0)
            self.frame1.tkraise()
        elif frame == frames["w trakcie"]:
            self.frame2 = Frame2(self, self.changeScreen)
            self.frame2.grid(row=0, column=0)
            self.frame2.tkraise()
        elif frame == frames["skonczone"]:
            pass

    def startApp(self):
        self.menuPage.tkraise()
        self.mainloop()


app = App()

app.startApp()