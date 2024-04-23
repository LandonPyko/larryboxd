from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "hello"

app.config['SESSION_COOKIE_NAME'] = 'session'  # Name of the session cookie
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Limit cookie access to HTTP requests
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # SameSite policy for cookies

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'larryboxd'

mysql = MySQL(app)

# Home Page
@app.route("/", methods = ["POST", "GET"])
def front_page():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

# Login/Register Account: ============================
@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/account_success", methods = ["POST"])
def account_success():
    username = request.form.get("username")
    password = request.form.get("password")
    favorite_movie = request.form.get("favorite_movie")
    age = request.form.get("age")

    session["username"] = username
    session["password"] = password
    session["favorite_movie"] = favorite_movie
    session["age"] = age

    cursor = mysql.connection.cursor()

    query= "INSERT INTO users (username, password, favorite_movie, age) VALUES (%s, %s, %s, %s)"
    cursor.execute(query,(username,password,favorite_movie,age,))
    mysql.connection.commit()
    
    cursor.close()

    return redirect(url_for("front_page"))

@app.route("/login", methods = ["GET","POST"])
def login():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        return redirect(url_for("front_page"))

@app.route("/login_info", methods = ["GET","POST"])
def login_info():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = mysql.connection.cursor()

        query= "SELECT * FROM users WHERE username = %s"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        
        if result is not None:
            session["username"] = username
            session["password"] = password
            return redirect(url_for("front_page"))
        
        else:    
            return render_template("create_account.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("front_page"))

# Login/Register Account End: ============================

# Create Account:
@app.route("/review", methods = ["POST"])
def review():
    if session.get("username") is None:
        return redirect(url_for("login"))
    else:
        title = request.form.get("title")
        year = request.form.get("year_released")
        director = request.form.get("director")

        session["title"] = title
        session["year"] = year
        session["director"] = director

        return render_template("create_review.html")

@app.route("/create_review", methods = ["POST"])
def create_review():
    username = session["username"]
    title = session["title"]
    director = session["director"]
    year = session["year"]

    score = request.form.get("score")
    notes = request.form.get("notes")
    cursor = mysql.connection.cursor()

    query= "INSERT INTO reviews (username, title, year_released, director, rating, comments) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query,(username,title,year,director,score,notes,))
    mysql.connection.commit()
    
    cursor.close()

    session.pop("title", None)
    session.pop("director", None)
    session.pop("year", None)

    return render_template("review_created.html")

# Display movie search reults
@app.route("/movie_title_search", methods = ["POST"])
def movie_title_search():
    if request.method == "POST":
        
        title = request.form["title"]
        title = "%" + title + "%"
        director = request.form["director"]
        director = "%" + director + "%"
        year = request.form["year_released"]
        year = "%" + year + "%"
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM movies WHERE title LIKE %s AND director LIKE %s AND year_released LIKE %s"
        cursor.execute(query, (title,director,year,))
        results = cursor.fetchall()
        return render_template("search_results.html", results=results)

if __name__ == "__main__":
    app.run()