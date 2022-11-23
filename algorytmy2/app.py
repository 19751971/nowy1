import json
import sqlite3

from flask import Flask, render_template, session, redirect, request
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'sfguw479g49w78ytgyw54989fgw937f'


class LoginForm(FlaskForm):
    userLogin = StringField('Nazwa użytkownika: ', validators=[DataRequired()])
    userPass = PasswordField('Hasło: ', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


users = {
    1: {
        'userLogin': 'jmaslowski',
        'userPass': 'zaq1@WSX',
        'fname': 'Julian',
        'lname': 'Maslowski'
    }
}


@app.route('/')
def index():
    return render_template('index.html', title='Strona główna')


@app.route('/login', methods=['POST', 'GET'])
def logIn():
    login = LoginForm()
    if login.validate_on_submit():
        userLogin = login.userLogin.data
        userPass = login.userPass.data
        connection = sqlite3.connect('data/alg-db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT userLogin FROM users WHERE userLOGIN='{userLogin}' AND userPASS='{userPass}'")
        user = cursor.fetchone()
        connection.close()
        if user and session.get('categoryId'):
            session['userLogin'] = userLogin
            return redirect('dashboard?id=' + session.get('categoryId'))
        else:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='logowanie', login=login, userLogin=session.get('userLogin'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    id = request.args.get('id')
    session['categoryId'] = id
    connection = sqlite3.connect('data/alg-db')
    cursor = connection.cursor()
    if str(id) == "None":
        cursor.execute(f"SELECT * FROM categories")
        categories = cursor.fetchall()
        return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                               fname=users[1]['fname'], categories=categories, id=session.get('categoryId'))
    else:
        cursor.execute("SELECT * FROM categories WHERE id = {}".format(session.get('categoryId')))
        categories = cursor.fetchall()

    connection.close()
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                           fname=users[1]['fname'], categories=categories, id=session.get('categoryId'))


@app.route('/logOut')
def logOut():
    session.pop('userLogin')
    session.pop('categoryId')
    return redirect('login')
    id = request.args.get('id')
    session['categoryId'] = id
    connection = sqlite3.connect('data/alg-db')
    cursor = connection.cursor()
    if not id:
        cursor.execute(f"SELECT * FROM categories")
        categories = cursor.fetchall()
        return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                               categories=categories, id=session.get('categoryId'), firstName=session.get('firstName'))
    else:
        cursor.execute("SELECT * FROM categories WHERE id = {}".format(session.get('categoryId')))
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM subjects WHERE category = {}".format(session.get('categoryId')))
        subjects = cursor.fetchall()
        cursor.execute("SELECT * FROM topics")
        topics = cursor.fetchall()
    connection.close()
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                           categories=categories,
                           id=id, firstName=session.get('firstName'), subjects=subjects, topics=topics)


@app.route('/content')
def content():
    id = request.args.get('id')
    subject = request.args.get('subject')
    connection = sqlite3.connect('data/alg-contents')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contents WHERE id=" + id)
    contents = cursor.fetchall()
    connection.close()
    return render_template('content.html', title=subject, userLogin=session.get('userLogin'),
                           fname=users[1]['fname'], contents=contents)


if __name__ == '__main__':
    app.run(debug=True)
