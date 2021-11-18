# Simple Student Information System
# Blaire Mendoza (2019-0381)
# CCC181


from flask          import Flask, app, redirect, render_template
from database       import mysql
from colleges       import colleges
from courses        import courses


# Server instance
app = Flask(__name__)

# Connect to database
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'password'
app.config['MYSQL_DATABASE_DB']         = 'students'
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.secret_key                          = 'monkey'
mysql.init_app(app)


app.register_blueprint(colleges)
app.register_blueprint(courses)


# Home page
# Shows students list
@app.route('/')
def home():
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM students ORDER BY last_name')
    data1 = cur.fetchall()
    cur.execute('SELECT course_code, course_name FROM courses')
    data2 = cur.fetchall()
    cur.close()
    
    # data1 -> students list | data2 -> course dropdown
    return render_template('home.html', students=data1, courses=data2)
    
    


if __name__ == '__main__':
    app.run(debug = True)