import tkinter as tk
from mysql.connector import connection
import os
from dotenv import load_dotenv


load_dotenv()
mysqlData = {
"MYSQL_USER" : os.getenv('MYSQL_USER'),
"MYSQL_PASSWORD":os.getenv('MYSQL_PASSWORD'),
"MYSQL_HOST" : os.getenv('MYSQL_HOST'),
"MYSQL_DATABASE": os.getenv('MYSQL_DATABASE')
}

frames = {
    "do przeczytania": "do_przeczytania",
    "w trakcie": "w_trakcie",
    "skonczone": "skonczone",
    "menu": "menu"
}
actionsNames = {
    "delete" : "Usuń",
    "mark_as_reading": "Czytaj",
    "finish_book": "Przeczytana",
    "rate_book": "Oceń"

}
colors = {
    "lightgreen": "#C1CFA1",
    "darkgreen" : "#A5B68D",
    "brown" : "#B17F59",
    "beige": "#EDE8DC"
}
class BackButton(tk.Button):
    def __init__(self,parent, changeFrame):
        super().__init__(parent)
        self.changeFrame = changeFrame
        self.configure(text="<", command=self.goToMenu, background=colors["beige"])
    def goToMenu(self):
        self.changeFrame(frames["menu"])

class TopFrameComponent(tk.Frame):
    def __init__(self, parent, changeScreenFunction, screenName):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        self.titleLabel2 = tk.Label(self, text=screenName, bg=colors["beige"], fg=colors["brown"])
        self.backBtn = BackButton(self, changeScreenFunction)

        self.titleLabel2.grid(row=0, column=1, sticky="NSEW")
        self.backBtn.grid(row=0, column=0, sticky="NEW")

class BookListGenerator(tk.Frame):
    def __init__(self, parent, books, selectQuery, actionName):
        super().__init__(parent)
        self.books = books
        self.selectQuery = selectQuery
        self.actionName = actionName

        self.booksListFrame = tk.Frame(self, background=colors["beige"])
        self.booksListFrame.pack(side=tk.TOP, expand=True,fill="both")
        self.currentPage = 1
        self.booksChunks = [self.books[x:x + 7] for x in range(0, len(self.books), 7)]
        self.booksChunksLength = len(self.booksChunks)


        if len(self.booksChunks) >= 1:
            self.onePageBooksList(self.booksListFrame, self.booksChunks[0])
            self.bottomPageInfo = f"{self.currentPage}/{len(self.booksChunks)}"
        else:
            self.noBooksLabel = tk.Label(self.booksListFrame, text="no books")
            self.bottomPageInfo = f"{self.currentPage}/{1}"
            self.noBooksLabel.pack()


        self.pageChangeButtonsFrame = tk.Frame(parent, height=30, background=colors["brown"])
        self.pageChangeButtonsFrame.pack(side=tk.BOTTOM, fill="x")
        self.bottomPageCounter(self.pageChangeButtonsFrame)
    def onePageBooksList(self, parent, onePageBookList):
        self.onePageFrame = tk.Frame(parent)

        for book in onePageBookList:
            # self.listedBook = BookFrame(parent, book[0],book[1],self.refreshScreen, self.bookActionFunction, self.selectQuery  )
            self.listedBook = BookFrame(parent, book[0], book[1], self.bookActionFunction, self.actionName)
            self.listedBook.pack(fill="x", pady=2.5)
        self.onePageFrame.pack()
    def bottomPageCounter(self, parent):

        self.buttonBack = tk.Button(parent, text="<", state=tk.DISABLED, command=self.changePageBack)
        pageLabel = tk.Label(parent, text=self.bottomPageInfo)
        self.buttonNext = tk.Button(parent, text=">", command=self.changePageNext)

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.rowconfigure(0, weight=1)
        self.buttonBack.grid(row=0, column=0)
        pageLabel.grid(row=0, column=1)
        self.buttonNext.grid(row=0, column=2)

    def changePageBack(self):
            if self.currentPage > 1:
                self.onePageFrame.destroy()
                for widget in self.booksListFrame.winfo_children():
                    widget.destroy()
                self.currentPage -=1
                self.buttonBack.configure(state=tk.ACTIVE)
                if self.currentPage < len(self.booksChunks):
                    self.buttonNext.configure(state="active")
                else:
                    self.buttonNext.configure(state="disabled")
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
        self.booksChunks = [self.books[x:x + 7] for x in range(0, len(self.books), 7)]
        self.booksChunksLength = len(self.booksChunks)

        if self.booksChunksLength < self.currentPage:
            self.currentPage = self.booksChunksLength

        # self.onePageFrame.destroy()
        for widget in self.booksListFrame.winfo_children():
            widget.destroy()
        for widget in self.pageChangeButtonsFrame.winfo_children():
            widget.destroy()


        if len(self.booksChunks) > 0:
            self.onePageBooksList(self.booksListFrame, self.booksChunks[self.currentPage - 1])
        else:
            print("????")

        self.bottomPageInfo = f"{self.currentPage}/{self.booksChunksLength}"
        self.bottomPageCounter(self.pageChangeButtonsFrame)
    def bookActionFunction(self, bookId, actionName):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()

        if actionName == actionsNames["delete"]:
            query = "DELETE FROM `book` WHERE `book`.`id` = %s"
            query_data = (str(bookId))
            cursor.execute(query, (query_data,))
            cnx.commit()

            query2 = self.selectQuery
            cursor.execute(query2)

            self.books.clear()
            for i in cursor:
                self.books.append(i)
        elif actionName == actionsNames["mark_as_reading"] :
            query = "UPDATE book SET reading_status = 'in-progress' WHERE book.id = %s"
            query_data = (str(bookId))
            cursor.execute(query, (query_data,))
            cnx.commit()

            query2 = self.selectQuery
            cursor.execute(query2)

            self.books.clear()
            for i in cursor:
                self.books.append(i)
        elif actionName == actionsNames["finish_book"]:
            query = "UPDATE book SET reading_status = 'finished' WHERE book.id = %s"
            query_data = (str(bookId))
            cursor.execute(query, (query_data,))
            cnx.commit()

            query2 = self.selectQuery
            cursor.execute(query2)

            self.books.clear()
            for i in cursor:
                self.books.append(i)
        elif actionName == actionsNames["rate_book"]:
            self.ratePupUp = tk.Frame(self, width=100, height=100, background="pink")
            rateLabel = tk.Label(self.ratePupUp, text="")
            self.ratePupUp.pack(anchor="center")

        self.refreshScreen()
        cnx.close()




class BookFrame(tk.Frame):

    def __init__(self, parent, bookId, title, bookActionFunction,  actionName):
        print(actionName)
        super().__init__(parent)
        self.bookId = bookId
        self.title = title

        self.bookTitle = tk.Label(self, text=self.title)
        self.deleteButton = tk.Button(self, text=actionsNames["delete"], background="red", command= lambda: bookActionFunction(self.bookId, actionsNames["delete"]))
        self.actionButton = tk.Button(self, text=actionName, background=colors["lightgreen"], command=lambda: bookActionFunction(self.bookId, actionName))

        self.configure(height=40, background=colors["beige"])

        self.bookTitle.pack(side=tk.LEFT)
        self.deleteButton.pack(side=tk.RIGHT)
        self.actionButton.pack(side=tk.RIGHT)
