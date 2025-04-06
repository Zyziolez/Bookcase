import asyncio
import tkinter as tk
from mysql.connector import connection
from data import frames, mysqlData, colors, actionsNames
from tkinter import simpledialog

class BackButton(tk.Button):
    def __init__(self,parent, changeFrame):
        super().__init__(parent)
        self.changeFrame = changeFrame
        self.configure(text="<", command=self.goToMenu, background=colors["beige"], bd=0, foreground=colors["brown"], font=("Outfit", 12, "bold"))
    def goToMenu(self):
        self.changeFrame(frames["menu"])

class TopFrameComponent(tk.Frame):
    def __init__(self, parent, changeScreenFunction, screenName):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        self.titleLabel2 = tk.Label(self, text=screenName, bg=colors["beige"], fg=colors["brown"], font=("Outfit", 12))
        self.backBtn = BackButton(self, changeScreenFunction)

        self.titleLabel2.grid(row=0, column=1, sticky="NSEW")
        self.backBtn.grid(row=0, column=0, sticky="NSEW")

class BookListGenerator(tk.Frame):
    def __init__(self, parent, books, selectQuery, actionName):
        super().__init__(parent)
        self.books = books
        self.selectQuery = selectQuery
        self.actionName = actionName

        self.booksListFrame = tk.Frame(self, background=colors["beige"])
        self.booksListFrame.pack(side=tk.TOP, expand=True,fill="both")
        self.currentPage = 1
        self.booksMax = lambda: 7 if actionName == actionsNames["mark_as_reading"] else 9
        self.booksChunks = [self.books[x:x + self.booksMax()] for x in range(0, len(self.books), self.booksMax())]
        self.booksChunksLength = len(self.booksChunks)

        self.pageChangeButtonsFrame = tk.Frame(parent, height=30, background=colors["beige"])
        if len(self.booksChunks) >= 1:
            self.onePageBooksList(self.booksListFrame, self.booksChunks[0])
            self.pageString = tk.StringVar(self.pageChangeButtonsFrame, f"{self.currentPage}/{len(self.booksChunks)}")
        else:
            self.noBooksLabel = tk.Label(self.booksListFrame, text="no books")
            self.pageString = tk.StringVar(self.pageChangeButtonsFrame, f"{self.currentPage}/{1}")
            self.noBooksLabel.pack()



        self.pageChangeButtonsFrame.pack(side=tk.BOTTOM, fill="x")
        self.bottomPageCounter(self.pageChangeButtonsFrame)
    def onePageBooksList(self, parent, onePageBookList):
        self.onePageFrame = tk.Frame(parent)

        for book in onePageBookList:
            # self.listedBook = BookFrame(parent, book[0],book[1],self.refreshScreen, self.bookActionFunction, self.selectQuery  )
            self.listedBook = BookFrame(parent, book[0], book[1], book[3], self.bookActionFunction, self.actionName)
            self.listedBook.pack(fill="x", pady=2.5)
        self.onePageFrame.pack()
    def bottomPageCounter(self, parent):

        self.buttonBack = tk.Button(parent, text="<", state=tk.DISABLED, background=colors["beige"], command=self.changePageBack, bd=0, font=("Outfit", 12, "bold"))
        pageLabel = tk.Label(parent, textvariable=self.pageString, background=colors["beige"], font=("Outfit", 12))
        self.buttonNext = tk.Button(parent, text=">",  command=self.changePageNext, background=colors["beige"], bd=0, font=("Outfit", 12, "bold"))

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.rowconfigure(0, weight=1)
        self.buttonBack.grid(row=0, column=0)
        pageLabel.grid(row=0, column=1)
        self.buttonNext.grid(row=0, column=2)

    def changePageBack(self):
            if self.currentPage > 1:
                self.currentPage -= 1
                self.refreshScreen()

    def changePageNext(self):
        if self.currentPage < len(self.booksChunks):
            self.currentPage += 1

            self.refreshScreen()

    def refreshScreen(self):

        self.booksChunks = [self.books[x:x + self.booksMax()] for x in range(0, len(self.books), self.booksMax())]
        self.booksChunksLength = len(self.booksChunks)



        if self.booksChunksLength < self.currentPage:
            self.currentPage = self.booksChunksLength

        for widget in self.booksListFrame.winfo_children():
            widget.destroy()


        if len(self.booksChunks) > 0:
            self.onePageBooksList(self.booksListFrame, self.booksChunks[self.currentPage - 1])
        else:
            self.onePageBooksList(1, [])

        self.pageString.set(f"{self.currentPage}/{self.booksChunksLength}")
        if self.currentPage == self.booksChunksLength:
            self.buttonNext.configure(state=tk.DISABLED)
        else:
            self.buttonNext.configure(state=tk.ACTIVE)

        if self.currentPage == 1:
            self.buttonBack.configure(state=tk.DISABLED)
        else:
            self.buttonBack.configure(state=tk.ACTIVE)
    def bookActionFunction(self, bookId, actionName):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()

        if actionName == actionsNames["delete"]:
            query_data = (str(bookId))
            deleteReview = "DELETE FROM `book_review` WHERE `book_review`.`bookID` = %s"

            query = "DELETE FROM `book` WHERE `book`.`id` = %s"
            cursor.execute(deleteReview, (query_data,))
            cnx.commit()
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
            ratingAnswer = simpledialog.askinteger("Input","How do you rate the book?", parent=self, minvalue=0, maxvalue=10)
            query = "INSERT INTO `book_review`(`id`, `rating`, `content`, `bookID`) VALUES (null,%s,'',%s)"
            query_data = (str(ratingAnswer), str(bookId))
            cursor.execute(query, query_data)
            cnx.commit()

        self.refreshScreen()
        cnx.close()




class BookFrame(tk.Frame):

    def __init__(self, parent, bookId, title, readingStatus, bookActionFunction,  actionName):
        super().__init__(parent)
        self.bookId = bookId
        self.title = title
        self.rating = None

        if readingStatus == "finished":
            asyncio.run(self.getRating())

        self.bookTitle = tk.Label(self, text=self.title, background=colors["darkbeige"], fg="white", font=("Outfit", 12))
        self.deleteButton = tk.Button(self, text=actionsNames["delete"], background=colors["red"], bd=0, fg="white",
                                      command=lambda: bookActionFunction(self.bookId, actionsNames["delete"]) )
        self.actionButton = tk.Button(self, text=actionName, background=colors["green"],
                                      command=lambda: bookActionFunction(self.bookId, actionName), bd=0, fg="white")

        if self.rating != None:
            self.actionButton.configure(state="disabled")
            self.bookTitle.configure(text=f"{self.rating}/10 - {self.title}")
        self.configure(height=40, background=colors["darkbeige"])

        self.bookTitle.pack(side=tk.LEFT)
        self.deleteButton.pack(side=tk.RIGHT)
        self.actionButton.pack(side=tk.RIGHT)
    async def getRating(self):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()
        query2 = ("select * from book_review where bookID = %s")
        queryData = (self.bookId)
        cursor.execute(query2, (queryData,))

        for i in cursor:
            self.rating = i[1]

        cnx.close()

