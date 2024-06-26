# 3. Develop a Flask app that uses URL parameters to display dynamic content.

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/greet/<name>')
def home(name):
    return render_template('greet.html', name = name)



if __name__ == '__main__':
    app.run(debug = True, port = 8001)