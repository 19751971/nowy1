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
        if user:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='logowanie', login=login, userLogin=session.get('userLogin'))


@app.route('/dashboard')
def dashboard():
    connection = sqlite3.connect('data/alg-db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM categories")
    categories = cursor.fetchall()
    connection.close()
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                           fname=users[1]['fname'], categories=categories)


@app.route('/logOut')
def logOut():
    session.pop('userLogin')
    return redirect('login')


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
