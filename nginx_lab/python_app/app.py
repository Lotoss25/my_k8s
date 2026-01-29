import time
import os
import socket
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    # Ми читаємо налаштування з "повітря" (змінних середовища), які передасть Docker
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

@app.route('/')
def hello():
    hostname = socket.gethostname()
    count = 0

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Створюємо таблицю, якщо її ще нема (це грубо, але для лаби ок)
        cur.execute('CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INTEGER)')
        
        # Перевіряємо, чи є вже лічильник
        cur.execute('SELECT count FROM visits WHERE id = 1;')
        result = cur.fetchone()
        
        if result:
            count = result[0] + 1
            cur.execute('UPDATE visits SET count = %s WHERE id = 1;', (count,))
        else:
            count = 1
            cur.execute('INSERT INTO visits (id, count) VALUES (1, 1);')
            
        conn.commit()
        cur.close()
        conn.close()
        
        db_status = "Connected to PostgreSQL! 🟢"
    except Exception as e:
        db_status = f"Database Error: {str(e)} 🔴"

    return f"""
    <h1>Hello from Python! 🐍</h1>
    <p>Container ID: <b>{hostname}</b></p>
    <p>Database Status: <b>{db_status}</b></p>
    <h2>Visitor Count: {count}</h2>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
