import mysql.connector
from config import settings

conn = mysql.connector.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
)
if conn:
  print("connection established")

cursor = conn.cursor(dictionary=True)
