from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/output', methods=['POST'])
def output():
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')
    gender = request.form.get('gender')
    newsletter = 'Yes' if request.form.get('newsletter') else 'No'
    
    return render_template('result.html', name=name, email=email, age=age, gender=gender, newsletter=newsletter)

if __name__ == '__main__':
    app.run(debug=True, port=8001)