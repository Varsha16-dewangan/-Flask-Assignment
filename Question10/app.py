from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Intentionally raising an exception to trigger a 500 error
    raise Exception("An intentional error")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error), 500

if __name__ == '__main__':
    app.run(debug=False, port=8001)
