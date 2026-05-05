import pymysql
from bottle import route, run

connection = pymysql.connect(
host='localhost',
user = 'root' ,
password = 'sasa' ,
database = 'lab3db'
)


@route('/')
def index():
    return "Η συνδεση με την βαση ειναι ετοιμη."

run(host='localhost' , port=8080, debug = True)