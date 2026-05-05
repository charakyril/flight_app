# flight_app

connection = pymysql.connect(
host='localhost',
user = 'root' ,
password = 'password' ,
database = 'flights'
)
εκανα την συνδεση σε workbench server και της ιστοσελιδας ωστε να ξεκινησουμε τα ερωτηματα . εβαλα στο database την βαση flights στην οποια πρεπει να δουλευουμε τα ερωτηματα. απο οτι εχω καταλαβει για να τσεκαρει αν δουλευει καποιος πρεπει να βαλει τον κωδικο του pc του οπου εχει αποθηκευσει το flights και να τρεξει μετα python app.py ή python3 app.py αναλογα το version της python που εχεις κατεβασει και να μπεις στην ιστοσελιδα http://localhost:8080/  οπου εμφανιζει ενα μηνυμα για το test της συνδεσης

import pymysql
from bottle import route, run,
template, request, static_file
bottle ειναι τα αρχεια template: αν βαλουμε εκει τον κωδικα html
request: Για αυτα που ζητα ο χρηστης
static_file : αν χρειαστουν στατικα αρχεια(πχ. για τα γραφικα της ιστοσελιδας)

-> όλα τα αρχεία της εφαρμογής όπως την έχετε υπολοιήσει, (πχ app.py, templates, 
static, κτλ ).  



@route('/findAirlineByAge/<x>/<y>')
def find_airline(x,y):
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT airline_id, COUNT(*) FROM passengers WHERE age BETWEEN %s AND %s GROUP BY airline_id", (x,y))

    result = cursor.fetchall()

    return str(result)

    για την ασκηση 1: findAirlinebyAge: Βρείτε την αεροπορική εταιρεία με τους περισσότερους ταξιδιώτες με ηλικία 
μικρότερη από Χ και μεγαλύτερη από Υ. Η συνάρτηση αυτή παίρνει ως ορίσματα δύο ακέραιους 
αριθμούς Χ, Υ και επιστρέφει:  
1. Το όνομα της αεροπορικής εταιρείας  
2. Το πλήθος των ταξιδιωτών που ικανοποιούν την συνθήκη  
3. Το πλήθος των αεροσκαφών αεροπορικής εταιρείας 

με βαση αυτo: from bottle import route, run
import sys, os 
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',  # use your own user
                             password='sasa', # use your own password
                             database='labtest') # use your own test database schema

@route('/todo')
def todo():
    # prepare a cursor object using cursor() method
    cursor = connection.cursor()
    cursor.execute("SELECT task FROM todo WHERE status LIKE '1'")
    result = cursor.fetchall()
    print(result)
    return str(result)
(FRONTISTIRIO 4)  


run(host='localhost', port=8080, debug=True) -> στο τελος του py αρχειου 


