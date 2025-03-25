import asyncio
import tkinter as tk
from components import mysqlData, BookListGenerator, TopFrameComponent
from mysql.connector import connection
class Frame2(tk.Frame):
    def __init__ (self, parent, changeScreenFunction):
        super().__init__(parent)
        self.changeScreen = changeScreenFunction
        self.books = []
        self.grid(column=0, row=0, padx=25, pady=25, sticky="NSEW")

        self.upFrame = TopFrameComponent(self, changeScreenFunction)

        self.configure(background="blue")
        asyncio.run(self.getBooks2())

        self.generator = BookListGenerator(self, self.books,
                                           "select * from book where reading_status = 'in-progress'")
        self.upFrame.pack(fill="x")
        self.generator.pack(expand=True, fill="both")
    async def getBooks2(self):
        cnx = connection.MySQLConnection(
            user=mysqlData["MYSQL_USER"], password=mysqlData["MYSQL_PASSWORD"],
            host=mysqlData["MYSQL_HOST"], database=mysqlData["MYSQL_DATABASE"]
        )
        cursor = cnx.cursor()
        query2 = ("select * from book where reading_status = 'in-progress'")
        cursor.execute(query2)

        for i in cursor:
            self.books.append(i)

        cnx.close()
        return None