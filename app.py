import pymysql
from bottle import route, run,
template, request, static_file

connection = pymysql.connect(
host='localhost',
user = 'root' ,
password = 'password' ,
database = 'flights'
)


@route('/findAirlineByAge/<x>/<y>')
def find_airline(x,y):
    cursor = connection.cursor()
    cursor.execute("SELECT airline_id, COUNT(*) FROM passengers WHERE age BETWEEN %s AND %s GROUP BY airline_id", (x,y))
    result = cursor.fetchall()
    return str(result) 

    run(host='localhost', port=8080, debug=True)

    