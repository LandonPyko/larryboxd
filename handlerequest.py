from flask import Flask, render_template, request, session, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "hello"




app.config['MYSQL_HOST'] = 'mysql.eecs.ku.edu'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'



@app.route("/")
def front_page():
    return render_template("frontpage.html")

