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
    "beige": "#EDE8DC",
    "green": "#92E285",
    "red": "#DF7676",
    "darkbeige": "#E5DECF"
}