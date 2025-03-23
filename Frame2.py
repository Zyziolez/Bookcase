import asyncio
import tkinter as tk
from components import mysqlData, BookListGenerator
from mysql.connector import connection
class Frame2(tk.Frame):
    def __init__ (self, parent, changeScreenFunction, refreshScreen):
        super().__init__(parent)
        self.changeScreen = changeScreenFunction
        self.books = []

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.getBooks())
        loop.close()

        self.generator = BookListGenerator(self, refreshScreen, self.books,
                                           "select * from book where reading_status = 'in-progress'")
        self.generator.pack(expand=True, fill="both")
    async def getBooks(self):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()
        query2 = ("select * from book where reading_status = 'in-progress'")
        cursor.execute(query2)

        for i in cursor:
            self.books.append(i)