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
app.config['MYSQL_PASSWORD'] = 'Terabyter47m!'
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

# Create review of a movie
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

# Display movie search results
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
    
# Display reviews of profit making movies
@app.route("/profit", methods = ["POST"])
def profit():
    if request.method == "POST":
        # username = session["username"]
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM reviews, movies WHERE (movies.box_office_earnings - movies.budget) > 0 AND movies.title = reviews.title AND movies.director = reviews.director AND movies.year_released = reviews.year_released"
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("profit_results.html", results=results)

# Find director of a user's favorite movie
@app.route("/favorite_director", methods = ["POST"])
def favorite_director():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        if request.method == "POST":
            username = session["username"]
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM movies, users WHERE movies.title = users.favorite_movie AND users.username = %s"
            cursor.execute(query, (username,))
            results = cursor.fetchall()
            return render_template("director_results.html", results=results)
        
# Find movies by a given director
@app.route("/movies_by_director", methods = ["POST"])
def movies_by_director():
    if request.method == "POST":
            # username = session["username"]
            cursor = mysql.connection.cursor()
            director = request.form["director"]
            query = "SELECT * FROM movies, users WHERE movies.director = %s"
            cursor.execute(query, (director,))
            movies = cursor.fetchall()
            return render_template("movies_by_director.html", movies=movies)

#Find average rating of a movie
@app.route("/average_rating", methods = ["POST"])
def average_rating():
    if request.method == "POST":
            # username = session["username"]
            cursor = mysql.connection.cursor()
            movie = request.form["title"]
            query = "SELECT title, year_released, director, AVG(rating) FROM reviews WHERE title = %s GROUP BY title, year_released, director"
            cursor.execute(query, (movie,))
            results = cursor.fetchall()
            return render_template("average_results.html", results=results)

# Find all theaters playing a movie
@app.route("/theaters_by_movie", methods = ["POST"])
def theaters_by_movie():
    if request.method == "POST":
            # username = session["username"]
            cursor = mysql.connection.cursor()
            movie = request.form["title"]
            query = "SELECT * FROM plays WHERE plays.title = %s"
            cursor.execute(query, (movie,))
            movies = cursor.fetchall()
            return render_template("theater_results.html", movies=movies)
    
# Find all movies that played in a theater
@app.route("/movies_by_theater", methods = ["POST"])
def movies_by_theater():
    if request.method == "POST":
            # username = session["username"]
            cursor = mysql.connection.cursor()
            theater = request.form["address"]
            query = "SELECT * FROM plays WHERE plays.address = %s"
            cursor.execute(query, (theater,))
            movies = cursor.fetchall()
            return render_template("movies_by_theater_results.html", movies=movies)

# See all reviews of a movie
@app.route("/see_reviews",methods = ["POST"])
def see_reviews():
    title = request.form["title"]
    title = "%" + title + "%"
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM reviews WHERE title LIKE %s"
    cursor.execute(query,(title,))
    results = cursor.fetchall()
    return render_template("all_reviews.html", results=results)

if __name__ == "__main__":
    app.run()