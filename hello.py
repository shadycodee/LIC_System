from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask import jsonify

app = Flask(__name__)

# Set a secret key for the application when using 'flash'
app.secret_key = 'qWer#123ty'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'records'

mysql = MySQL(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']


        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('manage'))
        else:
            return render_template('admin_login.html', message='Invalid Credentials')
    return render_template('admin_login.html')

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        studentid = request.form['studentid']
        name = request.form['name']
        password = request.form['password']
        course = request.form['course']

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (studentid, name, password, course) VALUES (%s, %s, %s, %s)",
                    (studentid, name, password, course))
        mysql.connection.commit()
        cur.close()

        #return jsonify({"message": "Student registered successfully"})
        # Use flash to store a message for the next request
        flash("Student registered successfully")

        # Redirect to the 'manage' route (GET) after successful registration
        return redirect(url_for('manage'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT studentid, name, course FROM students")
    students = cur.fetchall()
    cur.close()

    return render_template('manage.html', students=students)


@app.route('/login')
def student_login():
    return render_template('student_login.html')



if __name__ == '__main__':
    app.run(debug=True)