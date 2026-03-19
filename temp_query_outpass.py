import pymysql, os
from dotenv import load_dotenv

load_dotenv('backend/.env')

conn = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT')),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cur = conn.cursor()
cur.execute("SELECT id, status FROM outpasses WHERE status IN ('pending_otp','pending') LIMIT 5")
rows = cur.fetchall()
print(rows)
cur.close()
conn.close()
