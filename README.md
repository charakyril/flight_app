import pymysql 
from bottle import route, 
run, template, request


# Σύνδεση με την βάση δεδομένων MySQL
connection = pymysql.connect(
host ='localhost',  # o server της βάσης τοπικά
user = 'root' ,     # όνομα χρήστη
password = 'password' , // βαζεις τον κωδικο σου στο workbench 
database = 'flights'
)
// ασκηση 1πρωτα βρισκει το airline με τους περισσοτερους αναμεσα στις ηλικιες x k y για να χρησιμοποιηθει για να βρω και τα αεροπλανα που εχει αυτη η εταιρια στο επομενο sql
@route('/findAirlineByAge/<x>/<y>')
def find_airline(x,y):
    age1 = int(x)
    age2 = int(y)

min_age = min(age1, age2)
max_age = max(age1, age2)

year_low = 2026 - max_age
year_high = 2026 - min_age // η ηλικια πρεπει να ειναι μεγαλυτερη απο y και μικροτερη απο x τα χ και υ ειναι ηλικιες αλλα στο sql θελει year of birth Για αυτο τα αλλαζω
    

    # cursor activation for the sql questions
    cursor = connection.cursor()
   
   
    sql = """
        SELECT a.name, COUNT(p.id), a.id
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
    result = cursor.fetchone()   // pairnei thn mia seira apo ton pinaka
    
    if result:
        a_name, a_id, p_count = result
        
        cursor.execute("SELECT COUNT(airplanes_id) FROM airlines_has_airplanes WHERE airlines_id = %s", (a_id, ))
        planes = cursor.fetchone()[0]
        return template('results', rows=[(a_name, p_count, planes)])

    return "No results found."



// ασκηση 2 Αεροδρόμιο με περισσότερους επισκέπτες
# για συγκεκριμένη airline και ημερομηνίες
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
            return template('results' , rows=result)
        return "No results found."
   
   
   
   
 #εκκίνηση του web server
run(host='localhost', port=8080, debug=True)  // αυτο το βαζω μια φορα στο τελος 



//// 
    if result:
        a_name, a_id, p_count = result
        
        cursor.execute("SELECT COUNT(airplanes_id) FROM airlines_has_airplanes WHERE airlines_id = %s", (a_id, ))
        planes = cursor.fetchone()[0]  // εδω αποθηκευουμε στην μεταβλητη την λυση απο το workbench
        return template('results', rows=[(a_name, p_count, planes)]) // και τα στελνω το results.ptl που ειναι το αρχειο μεσαμ στον φακελο views που θα γραψουμε την  html εγω αυτο καταλαβα οτι κανουμε 

    return "No results found." // αν δεν εχει καποιο αποτελεσμα 

    ΥΣ¨δεν ξερω αν πρεπει να χρησιμοποιησουμε post/get για την συνδεση εδω @route('/findAirportVisitors/<x>/<A>/<B>') αντι για <x>/<A>/<B> 
    και αν πρεπει να κανουμε σε καθε ερωτημα ενα try except για περιπτωση που δεν γινεται η συνδεση παντως αυτη ειναι η μορφη νομιζω θα βαλω μετα σχολια 

εγραψα ον κώδικα sql για τα 3 επόμενα πηρα σαν template αυτα που είχες γράψει εσυ στα πρώτα ερωτήματα δεν ξέρω ακόμα να το συνδέσω με python θα το κοιτάξω ή δες το εσυ εαν το έχεις καραλάβει ίσως














-- Query 1: Find airline with the highest number of travelers whose age is less than X and greater than Y.
-- Use the year_of_birth bounds: year_low = current_year - max(X,Y); year_high = current_year - min(X,Y)
SELECT a.name AS airline_name,
       COUNT(p.id) AS traveler_count
FROM passengers p, flights_has_passengers fhp, flights f, routes r, airlines a
WHERE p.id = fhp.passengers_id
  AND fhp.flights_id = f.id
  AND f.routes_id = r.id
  AND r.airlines_id = a.id
  AND p.year_of_birth > 1988  -- replace with year_low
  AND p.year_of_birth < 2002  -- replace with year_high
GROUP BY a.id, a.name
ORDER BY traveler_count DESC;

-- Query 2: Find total visitors per airport served by airline X between dates A and B.
SELECT air.name AS airport_name,
       COUNT(fhp.passengers_id) AS visitor_count
FROM airlines a, routes r, airports air, flights f, flights_has_passengers fhp
WHERE a.id = r.airlines_id
  AND r.destination_id = air.id
  AND f.routes_id = r.id
  AND fhp.flights_id = f.id
  AND a.name = 'Aegean Airlines'  -- replace with airline name
  AND f.date BETWEEN '2026-01-01' AND '2026-12-31'  -- replace with dates
GROUP BY air.id, air.name
ORDER BY visitor_count DESC;

-- Query 3: Find alternative flights for travel from city A to city B on date X for active airlines.
SELECT f.id AS flight_id,
       al.name AS airline_name,
       arr.name AS destination_airport,
       airpl.model AS airplane_model
FROM flights f, routes r, airlines al, airports arr, airports dep, airplanes airpl
WHERE f.routes_id = r.id
  AND r.airlines_id = al.id
  AND r.destination_id = arr.id
  AND r.source_id = dep.id
  AND f.airplanes_id = airpl.id
  AND dep.city = 'Athens'        -- replace with source city
  AND arr.city = 'Paris'         -- replace with destination city
  AND f.date = '2026-06-15'     -- replace with travel date
  AND al.active = 'Y';

-- Query 4: Find the N airlines with the highest number of flights.
SELECT a.name AS airline_name,
       a.code AS airline_code,
       COUNT(aa.airplanes_id) AS airplane_count,
       COUNT(f.id) AS flight_count
FROM airlines a, routes r, flights f, airlines_has_airplanes aa
WHERE a.id = r.airlines_id
  AND f.routes_id = r.id
  AND aa.airlines_id = a.id
  AND a.active = 'Y'
GROUP BY a.id, a.name, a.code
ORDER BY flight_count DESC;

-- Query 5: Update passenger tier categories for a specific airline.
-- First run the SELECT to confirm counts, then use the application to update the tier column.
SELECT p.id AS passenger_id,
       p.name,
       p.surname,
       COUNT(*) AS flight_count
FROM passengers p, flights_has_passengers fhp, flights f, routes r, airlines a
WHERE p.id = fhp.passengers_id
  AND fhp.flights_id = f.id
  AND f.routes_id = r.id
  AND r.airlines_id = a.id
  AND a.name = 'Aegean Airlines'  -- replace with airline name
GROUP BY p.id, p.name, p.surname
ORDER BY flight_count DESC;
