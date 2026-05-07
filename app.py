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

@route('/findAirlineByAge/<x>/<y>')
def find_airline(x,y):
    age1 = int(x)
    age2 = int(y)

    min_age = min(age1,age2)
    max_age = max(age1,age2)

    year_low = 2026 - max_age
    year_high = 2026 - min_age

    # cursor activation for the sql questions
    cursor = connection.cursor()
   
   
    sql = """
        SELECT a.name, a.id, COUNT(p.id)
        FROM passengers p ,
            flights_has_passengers  fhp, 
            flights f, 
            routes r, 
            airlines a
        WHERE p.id = fhp.passengers_id
          AND fhp.flights_id = f.id
          AND f.routes_id = r.id
          AND r.airlines_id = a.id
          AND p.year_of_birth BETWEEN %s AND %s
        GROUP BY a.id, a.name
        ORDER BY COUNT(p.id) DESC 
    """
    cursor.execute(sql, (year_low, year_high))
    result = cursor.fetchone()
    
    if result:
        a_name, a_id, p_count = result
        
        cursor.execute("SELECT COUNT(airplanes_id) FROM airlines_has_airplanes WHERE airlines_id = %s", (a_id, ))
        planes = cursor.fetchone()[0]
        return template('results', rows=[(a_name, p_count, planes)])

    return "No results found."



@route('/findAirportVisitors/<x>/<A>/<B>')
def find_airport_visitors(x,A,B):
        #x -> name of airline A -> date (YYY-MM-DD) B -> date (YYY-MM-DD)
        cursor = connection.cursor()

        sql = """
              SELECT air.name, COUNT(fhp.passengers_id)
              FROM airlines a, 
                   routes r, 
                   airports air, 
                   flights f, 
                   flights_has_passengers fhp
              WHERE a.id = r.airlines_id
                AND r.destination_id = air.id
                AND f.routes_id = r.id
                AND fhp.flights_id = f.id
                AND a.name = %s
                AND f.date BETWEEN %s AND %s
              GROUP BY air.id, air.name
              ORDER BY COUNT(fhp.passengers_id) DESC
              """

        cursor.execute(sql, (x, A, B))
        result = cursor.fetchone()

        if result:
            return template('results' , rows=[result])
        return "No results found."
   
   
   
   
 #εκκίνηση του web server
run(host='localhost', port=8080, debug=True)



