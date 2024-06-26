# Implement user sessions in a Flask app to store and display user-specific data.

from flask import Flask, request, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return (
            f"Logged in as {username}<br>"
            "<b><a href='/logout'>Click here to log out</a></b>"
        )
    
    return (
        "You are not logged in<br>"
        "<a href='/login'><b>Click here to log in</b></a>"
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    return render_template('session.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port = 8001)
