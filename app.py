import pymysql 
from bottle import route, 
run, template, request


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
    cursor.execute("SELECT airlines_id, COUNT(*) FROM passengers WHERE age BETWEEN %s AND %s GROUP BY airlines_id ORDER BY COUNT(*) DESC", (x,y))
    #παίρνει όλα τα αποτελέσματα
    result = cursor.fetchall()
    if result :
        top_row = result[0]
        airlines_id = top_row[0]
        passengers_count = top_row[1]
    
    
        #βρισκει το ονομα της αεροπορικης εταιριας
        cursor.execute("SELECT name FROM airlines WHERE id=%s", (airlines_id,))
        res_name = cursor.fetchone()
        airlines_name = res_name[0]

        #βρισκει το πληθος των αεροσκαφών:
        cursor.execute("SELECT COUNT(*) FROM airplanes WHERE airlines_id = %s", (airlines_id,))
        res_name = cursor.fetchone()
        planes_count = res_name[0]
        return template('result', name = airlines_name,p_count=passengers_count,airplanes_count = planes_count, x=x, y=y) 


@route('/findAirportVisitors/<x>/<A>/<B>')
    def find_airport_visitors(x,A,B):
        #x -> name of airline A -> date (YYY-MM-DD) B -> date (YYY-MM-DD)
        cursor = connection.cursor()
        cursor.execute("SELECT airlines_id FROM airlines WHERE name = %s", (x, ))
        airlines_row = cursor.fetchone()

        if not airlines_row:
            return "Η εταιρία δεν βρέθηκε στη βάση δεδομένων."
        
        airlines_id = airlines_row[0]

     # finding the airport and the number of passengers that travel between these dates on the airport and by the airline X 
        sql = """
            SELECT airports_name, 
        COUNT(*)
            FROM passengers
            WHERE airlines_id = %s
        AND flights_date BETWEEN %s AND %s 
            GROUP BY airports_name
            ORDER BY COUNT(*) DESC
        """
        cursor.execute(sql,(airlines_id, A, B))
        result = cursor.fetchone()
        if result:
            #result[0] is the airports_name
            #result[1] is the number of passengers 
            return template(
                'results.ptl',
                name=x, 
                airport = result[0],
                total = result[1],
                start = A, 
                end=B
        )
        else:
            return "Δεν βρεθηκαν δεδομένα για αυτό το χρονικό διάστημα."
                


    #εκκίνηση του web server
    run(host='localhost', port=8080, debug=True)



