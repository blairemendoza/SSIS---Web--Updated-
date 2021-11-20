from flask      import Blueprint, render_template, request, flash, url_for, redirect
from database   import mysql

# Setup blueprint
courses = Blueprint('courses', __name__, url_prefix='/courses')

# Courses main page
@courses.route('/')
def coursesindex():
     
    cur = mysql.get_db().cursor()
    cur.execute('''SELECT courses.course_code, courses.course_name, colleges.college_name, colleges.college_code
                   FROM courses, colleges
                   WHERE courses.college_code=colleges.college_code ORDER BY colleges.college_name''')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM colleges')
    data2 = cur.fetchall()
    cur.execute('SELECT COUNT(*) FROM courses')
    data3 = cur.fetchall()


    # courses -> courses list
    return render_template('courses.html', courses=data1, colleges=data2, count=data3)


# Courses functions
# Add course
@courses.route('/add', methods = ['POST'])
def addcourse():
    
    coursecode  = request.form['inputCourseCode']
    coursename  = request.form['inputCourseName']
    collegecode = request.form['inputCollegeCode']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''INSERT INTO courses
                       VALUES (%s, %s, %s)''', (coursecode, coursename, collegecode))
        mysql.get_db().commit()
        
        flash('Course has been successfully added.', 'success')
        return redirect(url_for('courses.coursesindex'))
        
    except Exception as e:
        print('Add course error: ' + str(e))
        
        flash('Course code already exists. Enter a unique course code.', 'error')
        return redirect(url_for('courses.coursesindex'))
    
# Update course
@courses.route('/update', methods = ['POST'])
def updatecourse():
    
    coursecode  = request.form['updateCourseCode']
    coursename  = request.form['updateCourseName']
    collegecode = request.form['updateCollegeCode']
    oldcode     = request.form['oldCourseCode']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''UPDATE courses
                       SET course_code=%s, course_name=%s, college_code=%s
                       WHERE course_code=%s''', (coursecode, coursename, collegecode, oldcode))
        mysql.get_db().commit()
        
        flash('Course has been successfully updated.', 'success')
        return redirect(url_for('courses.coursesindex'))
        
    except Exception as e:
        print('Update course error: ' + str(e))
        
        flash('Course code already exists. Enter a unique course code.', 'error')
        return redirect(url_for('courses.coursesindex'))
        
# Remove course
@courses.route('/remove/<string:course_code>')
def removecourse(course_code):
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('DELETE FROM courses WHERE course_code=%s', (course_code,))
        mysql.get_db().commit()
        
        flash('Course has been successfully removed.', 'success')
        return redirect(url_for('courses.coursesindex'))

    except Exception as e:
        print('Remove course error: ' + str(e))
        
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('courses.coursesindex'))
