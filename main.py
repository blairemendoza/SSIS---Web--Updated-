# Simple Student Information System
# Blaire Mendoza (2019-0381)
# CCC181


from flask          import Flask, render_template, request, flash, url_for, redirect
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


# Student functions
# Add student
@app.route('/add', methods = ['POST'])
def addstudent():
    
    idnumber    = request.form['inputIDNumber']
    lastname    = request.form['inputLastName']
    firstname   = request.form['inputFirstName']
    course      = request.form['inputCourse']
    year        = request.form['inputYearLevel']
    gender      = request.form['inputGender']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''INSERT INTO students
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                       (idnumber, lastname, firstname, course, year, gender))
        mysql.get_db().commit()
        
        flash('Student has been successfully added.', 'success')
        return redirect(url_for('home'))
        
    except Exception as e:
        print('Add student error: ' + str(e))
        
        flash('ID number already exists. Use a unique ID number.', 'error')
        return redirect(url_for('home'))

# Update student
@app.route('/update', methods = ['POST'])
def updatestudent():
    
    idnumber    = request.form['updateID']
    lastname    = request.form['updateLast']
    firstname   = request.form['updateFirstName']
    course      = request.form['updateCourse']
    year        = request.form['updateYearLevel']
    gender      = request.form['updateGender']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''UPDATE students
                       SET last_name=%s, first_name=%s, course=%s, year_level=%s, gender=%s
                       WHERE id_number=%s''',
                       (lastname, firstname, course, year, gender, idnumber))
        mysql.get_db().commit()
        
        flash('Student has been successfully updated.', 'success')
        return redirect(url_for('home'))
    
    except Exception as e:
        print('Update student error: ' + str(e))
        
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('home'))
    
# Remove student
@app.route('/remove/<string:id_number>')
def removestudent(id_number):
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('DELETE FROM students WHERE id_number=%s', (id_number,))
        mysql.get_db().commit()
        
        flash('Student has been successfully removed.', 'success')
        return redirect(url_for('home'))
    
    except Exception as e:
        print('Remove student error: ' + str(e))
        
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug = True)