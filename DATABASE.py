import mysql.connector
import pymysql.cursors

def mydb():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="squeezo",
            charset="utf8mb4",
            cusorclass=pymysql.cursors.Cursor
        )
        return connection
    except mysql.connector.Error as e:
        print(f"[DB ERROR] Database connection failed: {e}")
        raise
