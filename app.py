import pymysql
from flask import Flask, request, jsonify
app = Flask(__name__)

def db_connection():
    con = None
    try:
        con = pymysql.connect(host="localhost", database="book", user="root", password='', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
    except pymysql.Error as e:
        print(e)
    
    return con

@app.route("/books", methods=["GET", "POST"])
def index():
    con = db_connection()
    cursor = con.cursor()
    if request.method == "GET":
        query = "SELECT * FROM books"
        cursor.execute(query)
        books = []
        li = cursor.fetchall()
        for i in li:
            x = {
                "bid": i["bid"],
                "author": i["author"],
                "language": i["language"],
                "title": i["title"]
            }
            books.append(x)
        
        if len(books) > 0:
            return jsonify(books)
        else:
            return "No books found"

    elif request.method == "POST":
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]
        query = "INSERT INTO books (author, language, title) VALUES(%s, %s, %s)"
        cursor.execute(query, (author, language, title))
        con.commit()

        return f"Book with {cursor.lastrowid} added successfully"

@app.route("/books/fetch/<int:bid>")
def fetchbook(bid):
    con = db_connection()
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE bid={bid}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        x = {
            "bid": res["bid"],
            "author": res["author"],
            "language": res["language"],
            "title": res["title"]
        }
        return jsonify(x)
    else:
        return "No such book found"

@app.route("/books/update/<int:bid>", methods=["POST"])
def updatebook(bid):
    con = db_connection()
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE bid={bid}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]
        query = "UPDATE books SET author=%s, language=%s, title=%s WHERE bid=%s"
        cursor.execute(query, (author, language, title, bid))
        con.commit()
        updatedbook = {
            "bid": bid,
            "author": author,
            "language": language,
            "title": title
        }
        return jsonify(updatedbook)
    else:
        return "No such book found"

@app.route("/books/delete/<int:bid>", methods=["POST"])
def deletebook(bid):
    con = db_connection()
    cursor = con.cursor()
    query = f"SELECT * FROM books WHERE bid={bid}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        x = {
            "bid": res["bid"],
            "author": res["author"],
            "language": res["language"],
            "title": res["title"]
        }
        query = f"DELETE FROM books WHERE bid={bid}"
        cursor.execute(query)
        con.commit()
        return jsonify(x)
    else:
        return "No such book found"

if __name__ == "__main__":
    app.run(debug=True)