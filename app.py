from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error

DATABASE = "C:/Users/21300/PycharmProjects/TutorWeb13dts/DB"

app = Flask(__name__)
app.secret_key = "abcdef"


def is_logged_in():
    if (session["first_name"] == None):
        print("Not Logged IN")
        return False
    else:
        print("Logged IN")
        return True

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


@app.route('/Schedule')
def render_schedule():
    con = connect_database(DATABASE)
    query = "SELECT Teacher_f_name, Student_f_name FROM TimeTable"
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    con.close()
    return render_template('Schedule.html', Sessions=results)





@app.route('/signup', methods=['POST','GET'])
def render_signup():

    if request.method == 'POST':

        try:
            fname = request.form.get('user_F_name')
            lname = request.form.get('user_L_name')
            email = request.form.get('user_email')
            pass1 = request.form.get('user_password')
            pass2 = request.form.get('user_password2')
            teachquestion = request.form.get('teachquestion')
            print("flag1")
            print(fname)
            if pass1 != pass2:
                return redirect("/signup?error=passwords+do+not+match")
            if len(pass1) < 8:
                return redirect("/signup?error=password+must+be+more+than+8+letters")

            con = connect_database(DATABASE)
            query_insert = ("INSERT INTO People (First_name, Last_name, Email, password, Teacher) "
                            "VALUES (?, ?, ?, ?, ?)")
            query_test = "SELECT * FROM People"
            cur = con.cursor()
            cur.execute(query_insert, (fname, lname, email, pass1, teachquestion))
            cur.execute(query_test)
            test_store = cur.fetchall()
            print(test_store)
            con.commit()


            return redirect("/login?message=signup+successful")

        except Exception as e:
            print(f"Signup error: {str(e)}")
            return redirect("/signup?error=registration+failed")

    # If it's a GET request, render the signup form
    return render_template("signup.html")
@app.route('/login', methods=['POST','GET'])

def render_login():
    if is_logged_in():
        return redirect('/menu/1')
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = request.form.get('user_password')

        con = connect_database(DATABASE)
        cur = con.cursor()
        query = "SELECT First_name, Last_name, Email, password FROM People WHERE email = ?"
        cur.execute(query,(email,))
        results = cur.fetchone()
        print(results)
        if password != results[3]:
            return redirect('/login/?message=Incorrctnameorpassword')
        session['email'] = results[2]
        session['first_name'] = results[0]
        session['last_name'] = results[1]
        print(session)
        return  redirect("/")
    return render_template('login.html')




if __name__ == '__main__':
    app.run()

print("WHYYYYY")