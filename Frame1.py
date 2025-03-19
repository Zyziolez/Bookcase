import tkinter as tk
from components import TopFrameComponent


class Frame1(tk.Frame):
    def __init__(self, parent, changeScreenFunction):
        super().__init__(parent)
        self.changeScreen = changeScreenFunction

        self.grid(column=0, row=0, padx=25, pady=25, sticky="NSEW")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        self.upFrame = TopFrameComponent(self, changeScreenFunction)

        self.inputFrame = tk.Frame(self, background="green", height=40)
        self.inputFrame.columnconfigure(0, weight=5)
        self.inputFrame.columnconfigure(1, weight=1)
        self.inputFrame.rowconfigure(0, weight=1)
        self.entryInput = tk.Entry(self.inputFrame)
        self.submitButton = tk.Button(self.inputFrame, text="Dodaj")

        self.entryInput.grid(row=0, column=0, sticky="NSEW")
        self.submitButton.grid(row=0, column=1, sticky="EW")

        self.upFrame.pack(fill="x")
        self.inputFrame.pack(fill="x", pady=20, padx=20)
        self.configure(background="red")

    def addNewBookButtonClick(self):
        pass