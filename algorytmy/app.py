from flask import Flask, render_template
from flask_bs4 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html',
                           title='Strona główna')


if __name__ == '__main__':
    app.run(debug=True)
