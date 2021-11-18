# Simple Student Information System
# Blaire Mendoza (2019-0381)
# CCC181


from flask          import Flask, app, redirect
from database       import mysql


# Server instance
app = Flask(__name__)

# Connect to database
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'password'
app.config['MYSQL_DATABASE_DB']         = 'students'
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
mysql.init_app(app)


@app.route('/')
def home():
    return 'Hello world'


if __name__ == '__main__':
    app.run(debug = True)