from flask import Flask, render_template, request, session, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "hello"

app.config['SESSION_COOKIE_NAME'] = 'session'  # Name of the session cookie
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Limit cookie access to HTTP requests
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # SameSite policy for cookies

app.config['MYSQL_HOST'] = 'mysql.eecs.ku.edu'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'

mysql = MySQL(app)

# Home Page
@app.route("/")
def front_page():
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

    query= "INSERT INTO user (username, password, favorite_movie, age) VALUES (%s, %s, %s, %s)"
    cursor.execute(query,(username,password,favorite_movie,age,))
    mysql.connection.commit()
    
    cursor.close()

    return render_template("account_success.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        return render_template("login_success.html")

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
            return render_template("login_success.html")
        
        else:    
            return render_template("create_account.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return render_template("index.html")

# Login/Register Account End: ============================

# Display movie search reults
@app.route("movie_title_search", methods = ["POST"])
def movie_title_search():
    if request.method == "POST":
        username = session["username"]
        title = "%" + request.form["title"] +"%"
        results = []
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM movies WHERE title LIKE %s"
        cursor.execute(query, (title,))
        results = cursor.fetchall()
        return render_template("search_results.html", results=results)

if __name__ == "__main__":
    app.run()