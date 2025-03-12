from flask import Flask, render_template
import sqlite3
from sqlite3 import Error


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




if __name__ == '__main__':
    app.run()

