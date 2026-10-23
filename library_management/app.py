from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def db():
    con = sqlite3.connect("library.db")
    con.row_factory = sqlite3.Row
    return con


# create tables
con = db()
con.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, username TEXT, password TEXT)")
con.execute("""CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id TEXT, book_name TEXT, book_number TEXT,
    student_name TEXT, issue_date TEXT, due_date TEXT)""")
con.commit()
con.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        con = db()
        con.execute("INSERT INTO users VALUES (?, ?, ?)",
                    (request.form["name"], request.form["username"], request.form["password"]))
        con.commit()
        con.close()
        return redirect("/login")
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        con = db()
        user = con.execute("SELECT * FROM users WHERE username=? AND password=?",
                           (request.form["username"], request.form["password"])).fetchone()
        con.close()
        if user:
            session["user"] = user["username"]
            return redirect("/dashboard")
        error = "Wrong username or password"
    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/issue", methods=["GET", "POST"])
def issue_book():
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        f = request.form
        con = db()
        cur = con.execute(
            "INSERT INTO books (book_id, book_name, book_number, student_name, issue_date, due_date) VALUES (?,?,?,?,?,?)",
            (f["book_id"], f["book_name"], f["book_number"], f["student_name"], f["issue_date"], f["due_date"]))
        con.commit()
        new_id = cur.lastrowid
        con.close()
        return redirect("/success/" + str(new_id))
    return render_template("issue_book.html")


@app.route("/success/<int:id>")
def success(id):
    if "user" not in session:
        return redirect("/login")
    con = db()
    book = con.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
    con.close()
    return render_template("success.html", book=book)


@app.route("/books")
def view_books():
    if "user" not in session:
        return redirect("/login")
    con = db()
    books = con.execute("SELECT * FROM books").fetchall()
    con.close()
    return render_template("view_books.html", books=books)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
