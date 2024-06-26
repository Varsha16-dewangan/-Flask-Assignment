from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

# Dictionary to store room information
rooms = {}

def generate_unique_code(length):
    """
    Generate a unique room code of specified length using uppercase ASCII characters.

    Args:
        length (int): Length of the room code to be generated.

    Returns:
        str: A unique room code.
    """
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/", methods=["POST", "GET"])
def home():
    """
    Handle the home page route. Clear session and manage form submissions for creating or joining a room.

    Returns:
        Response: Rendered home.html template or a redirect to the room page.
    """
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    """
    Handle the room page route.
    Check session for valid room and name, and render the room template.

    Returns:
        Response: Rendered room.html template or a redirect to the home page.
    """
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    """
    Handle incoming messages from clients. Broadcast the message to the room and store it in the room's message list.

    Args:
        data (dict): Dictionary containing the message data.
    """
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    """
    Handle a new connection. Join the user to their room and notify others in the room.

    Args:
        auth: Authentication data (not used in this function).
    """
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """
    Handle a disconnection. Leave the room, update the room's member count, and delete the room if empty.
    """
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


from flask import request, redirect, url_for
from datetime import datetime

# Assuming users_data is a global variable or otherwise accessible
users_data = {}  # Placeholder for actual data structure

@app.route("/update_msg/<string:user_id>", methods=['POST'])
def update_msg(user_id):
    if request.method == 'POST':
        req = request.form
        text = str(req['text'])
        msg_id = str(req['msg_id'])
        
        # Assuming chat_id is part of the user's data
        chat_id = users_data[user_id]['cid']
        
        timestamp = str(datetime.now())
        
        # Construct the message update payload
        dict_msg = {
            "op_type": "update_msg",
            "uid1": user_id,
            "uid2": chat_id,
            "text": text,
            "msg_id": msg_id,
            "timestamp": timestamp
        }
        
        # Update the message in the in-memory data structure
        if chat_id in users_data[user_id]['msg_list']:
            users_data[user_id]['msg_list'][chat_id][msg_id]['text'] = text
            users_data[user_id]['msg_list'][chat_id][msg_id]['timestamp'] = timestamp
        
        # Redirect or return response as needed
        return redirect(url_for('home', user_id=user_id))

    return "Invalid request method", 405




if __name__ == "__main__":
    # Run the Flask app with SocketIO support
    socketio.run(app, debug=True)


