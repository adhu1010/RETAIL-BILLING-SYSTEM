import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",      
        password="root",       
        database="retail"  
    )
    return conn

def get_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
