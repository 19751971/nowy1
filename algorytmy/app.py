from flask import Flask, render_template, session, redirect
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
        if userLogin == users[1]['userLogin'] and userPass == users[1]['userPass']:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='logowanie', login=login, userLogin=session.get('userLogin'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard', userLogin = session.get('userLogin'), fname=users[1]['fname'])

@app.route('/logOut')
def logOut():
    session.pop('userLogin')
    return redirect('login')
if __name__ == '__main__':
    app.run(debug=True)
