import mysql.connector
from config import *

def get_db():

    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = db.cursor(buffered=True)

    return db, cursor