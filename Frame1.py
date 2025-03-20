import tkinter as tk
from components import TopFrameComponent, books, BookListGenerator
from mysql.connector import connection
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MYSQL_USER= os.getenv('MYSQL_USER')
MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')
MYSQL_HOST=os.getenv('MYSQL_HOST')
MYSQL_DATABASE=os.getenv('MYSQL_DATABASE')

class Frame1(tk.Frame):
    def __init__(self, parent, changeScreenFunction, refreshScreen):
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
        self.submitButton = tk.Button(self.inputFrame, text="Dodaj", command=self.addNewBookButtonClick)

        self.entryInput.grid(row=0, column=0, sticky="NSEW")
        self.submitButton.grid(row=0, column=1, sticky="EW")

        self.generator = BookListGenerator(self, refreshScreen)

        self.upFrame.pack(fill="x")
        self.inputFrame.pack(fill="x", pady=20, padx=20)
        self.generator.pack(expand=True, fill="both")

    def addNewBookButtonClick(self):
        self.bookName = self.entryInput.get()
        self.entryInput.delete(0, tk.END)

        cnx = connection.MySQLConnection(
            user=MYSQL_USER, password=MYSQL_PASSWORD,
            host=MYSQL_HOST, database=MYSQL_DATABASE
        )
        cursor = cnx.cursor()
        query = ("INSERT INTO `book`(`id`, `name`, `date_of_submission`, `reading_status`) values (Null, %s, %s, 'not-started')")
        query_data = (self.bookName, datetime.today().strftime('%Y-%m-%d'))
        cursor.execute(query, query_data)
        cnx.commit()

        query2 = ("select * from book")
        cursor.execute(query2)

        books.clear()

        for i in cursor:
            books.append(i)

        self.generator.refreshScreen()
        cnx.close()
