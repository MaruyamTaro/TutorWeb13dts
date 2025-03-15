from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

DATABASE = "DB.db"
app = Flask(__name__)
def connect_database(db_file):
    """
    Creates a connection with the database
    :param db_file:
    :return: conn
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        print(f'an error when connecting the db')
    return


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu():
    return render_template('Schedule.html')

@app.route('/signup', methods=['POST','GET'])
def render_signup():
    if request.method == 'POST':
        fname = request.form.get('user_F_name').title().strip()
        lname = request.form.get('user_L_name').title().strip()
        email = request.form.get('user_email').lower().strip()
        pass1 = request.form.get('user_password')
        pass2 = request.form.get('user_password2')
        teachquestion = request.form.get('teachquestion')


        if pass1 != pass2:
            return redirect("\signup?error=passwords+do+not+match")

        if len(pass1) < 8:
            return redirect("\signup?error=password+must+be+more+than+8+letters")

        con = connect_database(DATABASE)
        query_insert = "INSERT INTO People (fname, lname, email, pass1, teachquestion) VALUES (?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query_insert, (fname, lname, email, pass1, teachquestion))



    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def render_login():
    return render_template('login.html')




if __name__ == '__main__':
    app.run()

