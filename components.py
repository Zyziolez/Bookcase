import tkinter as tk
from mysql.connector import connection
import os
from dotenv import load_dotenv


load_dotenv()

MYSQL_USER= os.getenv('MYSQL_USER')
MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')
MYSQL_HOST=os.getenv('MYSQL_HOST')
MYSQL_DATABASE=os.getenv('MYSQL_DATABASE')

books =[]

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

class BookListGenerator(tk.Frame):
    def __init__(self, parent, refreshScreen):
        super().__init__(parent)

        self.booksListFrame = tk.Frame(self, background="orange")
        self.booksListFrame.pack(side=tk.TOP, expand=True,fill="both")
        self.currentPage = 1
        self.booksChunks = [books[x:x + 7] for x in range(0, len(books), 7)]
        self.booksChunksLength = len(self.booksChunks)

        pageChangeButtonsFrame = tk.Frame(self, height=30, background="green")
        pageChangeButtonsFrame.pack(side=tk.BOTTOM, fill="x")
        self.buttonBack = tk.Button(pageChangeButtonsFrame, text="<", state=tk.DISABLED, command=self.changePageBack)
        pageLabel = tk.Label(pageChangeButtonsFrame, text=f"{self.currentPage}/{len(self.booksChunks)}")
        self.buttonNext = tk.Button(pageChangeButtonsFrame, text=">", command=self.changePageNext)

        pageChangeButtonsFrame.columnconfigure(0, weight=1)
        pageChangeButtonsFrame.columnconfigure(1, weight=1)
        pageChangeButtonsFrame.columnconfigure(2, weight=1)
        pageChangeButtonsFrame.rowconfigure(0, weight=1)
        self.buttonBack.grid(row=0, column=0)
        pageLabel.grid(row=0, column=1)
        self.buttonNext.grid(row=0, column=2)

        self.onePageBooksList(self.booksListFrame, self.booksChunks[0])
    def onePageBooksList(self, parent, onePageBookList):
        self.onePageFrame = tk.Frame(parent)

        for book in onePageBookList:
            self.listedBook = BookFrame(parent, book[0],book[1],self.refreshScreen  )
            self.listedBook.pack(fill="x", pady=2.5)
        self.onePageFrame.pack()

    def changePageBack(self):
            if self.currentPage > 1:
                self.onePageFrame.destroy()
                for widget in self.booksListFrame.winfo_children():
                    widget.destroy()
                self.currentPage -=1
                self.buttonBack.configure(state=tk.ACTIVE)
                if self.currentPage < len(self.booksChunks):
                    self.buttonNext.configure(state=tk.ACTIVE)
                if self.currentPage == 1:
                    self.buttonBack.configure(state="disabled")
                self.onePageBooksList(self.booksListFrame, self.booksChunks[self.currentPage - 1])
    def changePageNext(self):
        if self.currentPage < len(self.booksChunks):
            self.currentPage += 1
            self.onePageFrame.destroy()
            for widget in self.booksListFrame.winfo_children():
                widget.destroy()
            if self.currentPage > 1:
                self.buttonBack.configure(state="active")
            self.buttonNext.configure(state=tk.ACTIVE)
            if self.currentPage == len(self.booksChunks):
                self.buttonNext.configure(state="disabled")

            self.onePageBooksList(self.booksListFrame, self.booksChunks[self.currentPage - 1])

    def refreshScreen(self):
        self.booksChunks = [books[x:x + 7] for x in range(0, len(books), 7)]
        self.onePageFrame.destroy()
        for widget in self.booksListFrame.winfo_children():
            widget.destroy()
        self.onePageBooksList(self.booksListFrame, self.booksChunks[self.currentPage - 1])
        self.booksChunksLength = len(self.booksChunks)

class BookFrame(tk.Frame):
    def __init__(self, parent, bookId, title, refreshScreen):
        super().__init__(parent)
        self.bookId = bookId
        self.title = title
        self.refreshScreen = refreshScreen

        self.bookTitle = tk.Label(self, text=self.title, background="yellow")
        self.deleteButton = tk.Button(self, text="Delete", background="red", command=self.deleteBookFromList)

        self.configure(height=40)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0,weight=1)

        self.bookTitle.grid(row=0, column=0, sticky="NSW")
        self.deleteButton.grid(row=0, column=1, sticky="NSE")
    def deleteBookFromList(self):
        cnx = connection.MySQLConnection(
            user=MYSQL_USER, password=MYSQL_PASSWORD,
            host=MYSQL_HOST, database=MYSQL_DATABASE
        )
        cursor = cnx.cursor()
        query = "DELETE FROM `book` WHERE `book`.`id` = %s"
        query_data = (str(self.bookId))
        cursor.execute(query, (query_data,))
        cnx.commit()

        query2 = ("select * from book")
        cursor.execute(query2)

        books.clear()
        for i in cursor:
            books.append(i)

        self.refreshScreen()
        cnx.close()