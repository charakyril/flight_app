import pymysql 
from bottle import route, run,
template, request, static_file

# Σύνδεση με την βάση δεδομένων MySQL
connection = pymysql.connect(
host ='localhost',  # o server της βάσης τοπικά
user = 'root' ,     # όνομα χρήστη
password = 'password' ,
database = 'flights'
)

# route που δέχεται δύο παραμέτρους ηλικίας
@route('/findAirlineByAge/<x>/<y>')
def find_airline(x,y):
    # δημιουργία cursor για εκτέλεση SQL ερωτημάτων
    cursor = connection.cursor()
    # βρίσκεις πόσους επιβάτες έχει κάθε airline για επιβάτες με ηλικία απο x μέχρι y
    cursor.execute("SELECT airline_id, COUNT(*) FROM passengers WHERE age BETWEEN %s AND %s GROUP BY airline_id ORDER BY COUNT(*) DESC", (x,y))
    #παίρνει όλα τα αποτελέσματα
    result = cursor.fetchall()

    if result :
        top_row = result[0]
        airline_id = top_row[0]
        passengers_count = top_row[1]
    
    
        #βρισκει το ονομα της αεροπορικης εταιριας
        cursor.execute("SELECT name FROM airlines WHERE id=%s", (airline_id,))
        res_name = cursor.fetchone()
        airline_name = res_name[0]

        #βρισκει το πληθος των αεροσκαφών:
        cursor.execute("SELECT COUNT(*) FROM airplanes WHERE airline_id = %s", (airline_id,))
        res_name = cursor.fetchone()
        planes_count = res_name[0]
        return template('result', name = airline_name,p_count=passengers_count,airplanes_count = planes_count, x=x, y=y) 

    #εκκίνηση του web server
    run(host='localhost', port=8080, debug=True)

