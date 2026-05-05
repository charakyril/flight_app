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