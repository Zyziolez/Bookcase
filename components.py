import tkinter as tk

frames = {
    "do przeczytania": "do_przeczytania",
    "w trakcie": "w_trakcie",
    "skonczone": "skonczone",
    "menu": "menu"
}
class BackButton(tk.Button):
    def __init__(self,parent, changeFrame):
        super().__init__(parent)
        self.changeFrame = changeFrame
        self.configure(text="<", command=self.goToMenu)
    def goToMenu(self):
        self.changeFrame(frames["menu"])

class TopFrameComponent(tk.Frame):
    def __init__(self, parent, changeScreenFunction):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        self.titleLabel2 = tk.Label(self, text="frame1", fg="red", bg="pink")
        self.backBtn = BackButton(self, changeScreenFunction)

        self.titleLabel2.grid(row=0, column=1, sticky="NSEW")
        self.backBtn.grid(row=0, column=0, sticky="NEW")