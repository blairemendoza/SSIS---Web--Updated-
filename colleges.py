from flask      import Blueprint, render_template, request, flash, url_for, redirect
from database   import mysql

# Setup blueprint
colleges = Blueprint('colleges', __name__, url_prefix='/colleges')

# Colleges main page
@colleges.route('/')
def collegeindex():
    
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM colleges ORDER BY college_code')
    data = cur.fetchall()
    cur.close()
    
    # data -> colleges list
    return render_template('colleges.html', colleges=data)


# College functions
# Add college
@colleges.route('/add', methods = ['POST'])
def addcollege():
    
    collegecode = request.form['inputCollegeCode']
    collegename = request.form['inputCollegeName']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''INSERT INTO colleges
                       VALUES (%s, %s)''', (collegecode.upper(), collegename))
        mysql.get_db().commit()
        
        flash('College has been successfully added.', 'success')
        return redirect(url_for('colleges.collegeindex'))
        
    except Exception as e:
        print('Add college error: ' + str(e))
        
        flash('College code already exists. Enter a unique college code.', 'error')
        return redirect(url_for('colleges.collegeindex'))
    

# Update college
@colleges.route('/update', methods = ['POST'])
def updatecollege():
    
    collegecode = request.form['updateCollegeCode']
    collegename = request.form['updateCollegeName']
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('''UPDATE colleges
                       SET college_name=%s
                       WHERE college_code=%s''', (collegename, collegecode))
        mysql.get_db().commit()
        
        flash('College has been successfully updated.', 'success')
        return redirect(url_for('colleges.collegeindex'))
    
    except Exception as e:
        print('Update college error: ' + str(e))
        
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('colleges.collegeindex'))

# Remove college
@colleges.route('/remove/<string:college_code>')
def removecollege(college_code):
    
    try:
        cur = mysql.get_db().cursor()
        cur.execute('DELETE FROM colleges WHERE college_code=%s', (college_code,))
        mysql.get_db().commit()
        
        flash('College has been successfully removed.', 'success')
        return redirect(url_for('colleges.collegeindex'))
    
    except Exception as e:
        print('Remove college error: ' + str(e))
        
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('colleges.collegeindex'))
    