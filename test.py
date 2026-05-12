import pymysql
from bottle import Bottle, run, request, template

app = Bottle()

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",  # ← password we just set
    "database": "ergasia2",
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/test')
def test():
    try:
        conn = get_connection()
        conn.close()
        return "✅ Connected!"
    except Exception as e:
        return f"❌ Error: {e}"

run(app, host='localhost', port=8080, debug=True)