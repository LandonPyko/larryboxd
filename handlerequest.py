from flask import Flask, render_template, request, session, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "hello"

app.config['SESSION_COOKIE_NAME'] = 'session'  # Name of the session cookie
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Limit cookie access to HTTP requests
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # SameSite policy for cookies

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Terabyter47m!'
app.config['MYSQL_DB'] = 'larryboxd'

mysql = MySQL(app)

# Home Page
@app.route("/")
def front_page():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

# Login/Register Account: ============================
@app.route("/create_account")
def create_account():
    return render_template("createaccount.html")

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

    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        return render_template("index.html")

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
            return render_template("index.html")
        
        else:    
            return render_template("create_account.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return render_template("index.html")

# Login/Register Account End: ============================

# Create Account:
@app.route("/review")
def review():
    return render_template("create_review.html")

@app.route("/create_review")
def create_review():
    username = session["username"]
    title = request.form.get("title")
    director = request.form.get("director")
    year = request.form.get("year_released")
    score = request.form.get("score")
    notes = request.form.get("notes")
    cursor = mysql.connection.cursor()

    query= "INSERT INTO reviews (username, title, director, year, score, notes) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query,(username,title,director,year,score,notes,))
    mysql.connection.commit()
    
    cursor.close()

# Display movie search reults
@app.route("/movie_title_search", methods = ["POST"])
def movie_title_search():
    if request.method == "POST":
        username = session["username"]
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