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
