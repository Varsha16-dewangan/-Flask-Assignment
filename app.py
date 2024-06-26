from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Dictionary to store room information
rooms = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    session['username'] = request.form['username']
    return render_template('chat.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(data['username'])
    send(f"{data['username']} has joined the room.", room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)
    if room in rooms and data['username'] in rooms[room]:
        rooms[room].remove(data['username'])
    send(f"{data['username']} has left the room.", room=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    send({'username': session['username'], 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
