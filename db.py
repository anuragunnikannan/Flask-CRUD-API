import pymysql

con = pymysql.connect(host="localhost", database="book", user="root", password='', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

cursor = con.cursor()
query = "CREATE TABLE books(bid INTEGER PRIMARY KEY, author TEXT NOT NULL, language TEXT NOT NULL, title TEXT NOT NULL)"
cursor.execute(query)
con.close()