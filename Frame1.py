import tkinter as tk
from components import TopFrameComponent, BookListGenerator, mysqlData
from mysql.connector import connection
from datetime import datetime
import asyncio

class Frame1(tk.Frame):
    def __init__(self, parent, changeScreenFunction):
        super().__init__(parent)
        self.changeScreen = changeScreenFunction
        self.books = []


        self.grid(column=0, row=0, padx=25, pady=25, sticky="NSEW")


        self.upFrame = TopFrameComponent(self, changeScreenFunction)

        self.inputFrame = tk.Frame(self, background="green", height=40)
        self.inputFrame.columnconfigure(0, weight=5)
        self.inputFrame.columnconfigure(1, weight=1)
        self.inputFrame.rowconfigure(0, weight=1)
        self.entryInput = tk.Entry(self.inputFrame)
        self.submitButton = tk.Button(self.inputFrame, text="Dodaj", command=self.addNewBookButtonClick)

        self.entryInput.grid(row=0, column=0, sticky="NSEW")
        self.submitButton.grid(row=0, column=1, sticky="EW")

        asyncio.run(self.getBooks())

        self.generator = BookListGenerator(self, self.books, "select * from book where reading_status = 'not-started'")

        self.upFrame.pack(fill="x")
        self.inputFrame.pack(fill="x", pady=20, padx=20)
        self.generator.pack(expand=True, fill="both")

    async def getBooks(self):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()
        query2 = ("select * from book where reading_status = 'not-started'")
        cursor.execute(query2)

        for i in cursor:
            self.books.append(i)

        cnx.close()

    def addNewBookButtonClick(self):
        self.bookName = self.entryInput.get()
        self.entryInput.delete(0, tk.END)

        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()
        query = ("INSERT INTO `book`(`id`, `name`, `date_of_submission`, `reading_status`) values (Null, %s, %s, 'not-started')")
        query_data = (self.bookName, datetime.today().strftime('%Y-%m-%d'))
        cursor.execute(query, query_data)
        cnx.commit()

        query2 = ("select * from book where reading_status = 'not-started'")
        cursor.execute(query2)

        self.books.clear()

        for i in cursor:
            self.books.append(i)

        self.generator.refreshScreen()
        cnx.close()
