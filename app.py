import pymysql 
from bottle import route, run, template, request


# Σύνδεση με την βάση δεδομένων MySQL
connection = pymysql.connect(
host ='localhost',  # o server της βάσης τοπικά
user = 'root' ,     # όνομα χρήστη
password = 'password', # κωδικός πρόσβασης, 
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
          AND p.year_of_birth > %s
          AND p.year_of_birth < %s
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
        result = cursor.fetchall()

        if result:
            return template('results' , rows = result)
        return "No results found."
   
@route('/findAlternativeFlights/<A>/<B>/<X>')
def findAlternativeFlights(A,B,X):
        #Α πόλη αναχώρησης Β πόλη άφιξης Χ ημερομηνία που φτάνεισ τον προορισμό του 
        cursor = connection.cursor()

        sql = """
            SELECT f.id, al.alias, arr.name, airpl.model 
            FROM flights f, routes r, airlines al, airports arr, airports dep, airplanes airpl 
            WHERE f.routes_id = r.id
              AND r.airlines_id = al.id
              AND r.destination_id = arr.id
              AND r.source_id = dep.id
              AND f.airplanes_id = airpl.id
              AND dep.city = %s
              AND arr.city = %s
              AND f.date = %s
              AND  al.active = 'Y'
              """

        cursor.execute(sql, (x, A, B))
        result = cursor.fetchall()

        if result:
            return template('results' , rows = result)
        return "No results found."


@route('/findLargestAirlines/<N>')
def findLargestAirlines(N):
        #N ο αριθμός των εταιρειών με τισ περισσότερες πτήσεις 
        cursor = connection.cursor()

        sql = """
            SELECT a.name, a.code, COUNT(aa.airplanes_id), COUNT(f.id)
            FROM airlines a, routes r, flights f, airlines_has_airplanes aa
            WHERE a.id = r.airlines_id
            AND f.routes_id = r.id
            AND aa.airlines_id = a.id
            AND a.active = 'Y'
            GROUP BY a.id, a.name, a.code
            ORDER BY COUNT(f.id) DESC
            """

        cursor.execute(sql, (x, A, B))
        result = cursor.fetchall()

        if result:
            return template('results' , rows = result)
        return "No results found."
   
   
  @route('/findAlternativeFlights/<A>/<B>/<X>')
def findAlternativeFlights(A,B,X):
        #Α πόλη αναχώρησης Β πόλη άφιξης Χ ημερομηνία που φτάνεισ τον προορισμό του 
        cursor = connection.cursor()

        sql = """
            SELECT f.id, al.alias, arr.name, airpl.model 
            FROM flights f, routes r, airlines al, airports arr, airports dep, airplanes airpl 
            WHERE f.routes_id = r.id
              AND r.airlines_id = al.id
              AND r.destination_id = arr.id
              AND r.source_id = dep.id
              AND f.airplanes_id = airpl.id
              AND dep.city = %s
              AND arr.city = %s
              AND f.date = %s
              AND  al.active = 'Y'
              """

        cursor.execute(sql, (A, B, X))
        result = cursor.fetchall()

        if result:
          return template('results' , rows = result)
        return "No results found."


@route('/findLargestAirlines/<N>')
def findLargestAirlines(N):
        #N ο αριθμός των εταιρειών με τισ περισσότερες πτήσεις 
        cursor = connection.cursor()

        sql = """
            SELECT a.name, a.code, COUNT(aa.airplanes_id), COUNT(f.id)
            FROM airlines a, routes r, flights f, airlines_has_airplanes aa
            WHERE a.id = r.airlines_id
            AND f.routes_id = r.id
            AND aa.airlines_id = a.id
            AND a.active = 'Y'
            GROUP BY a.id, a.name, a.code
            ORDER BY COUNT(f.id) DESC
            """

        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
              n_results = result[:int(N)]
              return template('results' , rows = n_results)
        return "No results found."
   
   

@route('/updatePassengerStatus/<A>/<B>')
def updatePassengerStatus(A, B):
        #N ο αριθμός των εταιρειών με τισ περισσότερες πτήσεις 
        cursor = connection.cursor()

        try:
            try:
                cursor.execute("ALTER TABLE passengers ADD COLUMN tier VARCHAR(20)")
            except:
                pass

            sql = """
                 SELECT p.id , COUNT(*)
                 FROM passengers p, 
                      flights_has_passengers fhp, 
                      flights f, 
                      routes r, 
                      airlines a
                WHERE p.id = fhp.passengers_id
                    AND fhp.flights_id = f.id
                    AND f.routes_id = r.id
                    AND r.airlines_id = a.id
                    AND a.name = %s
                    GROUP BY p.id
                    """
            cursor.execute(sql,(A, ))

            results = cursor.fetchall()

            for passenger_id, flights_count in results:

            if flights_count <= 1:
                passenger_tier = "Basic"

            elif flights_count <= 4:
                passenger_tier = "Silver"

            elif flights_count == 5:
                passenger_tier = "Gold"

            else:
                passenger_tier = "Platinum"

            cursor.execute(
                    """
                    UPDATE passengers
                    SET tier = %s
                    WHERE id = %s 
                    """,
                    (passenger_tier, passenger_id)
                )

        connection.commit()
    except:
            connection.rollback()
            return "Error occured during update."

        sql_select = """
            SELECT name,surname, tier
            FROM passengers
            WHERE tier = %s
                  """
        cursor.execute(sql_select, (B, ))
        result = cursor.fetchall()
        return template('results', rows = result)


 #εκκίνηση του web server
run(host='localhost', port=8080, debug=True)



