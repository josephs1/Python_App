from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Game state
player = {"x": 100, "y": 100}  # Initial position of the rectangle

@app.route("/")
def game_screen():
    return render_template("game.html")  # Main screen

@app.route("/controller")
def controller():
    return render_template("controller.html")  # Controller screen

@socketio.on("move_player")
def handle_move(data):
    # Handle movement commands from the controller.
    global player
    direction = data.get("direction")
    speed = 10  # Movement speed

    # Update the player's position based on the direction
    if direction == "left":
        player["x"] = max(0, player["x"] - speed)
    elif direction == "right":
        player["x"] = min(780, player["x"] + speed)  # Prevent moving out of bounds
    elif direction == "up":
        player["y"] = max(0, player["y"] - speed)
    elif direction == "down":
        player["y"] = min(580, player["y"] + speed)  # Prevent moving out of bounds

    # Notify the main screen to update the rectangle's position
    socketio.emit("update_position", player)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


"""
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Game state
player = {"x": 100, "y": 100}  # Initial position of the rectangle

@app.route("/")
def game_screen():
    return render_template("game.html")  # Serve the game screen

@socketio.on("move_player")
def handle_move(data):
    # Update the player's position when notified by the client.
    global player
    player["x"] = data.get("x", player["x"])
    player["y"] = data.get("y", player["y"])

    # (Optional) Log the current state on the server
    print(f"Player moved to: {player}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
"""


"""from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Global variables to track users and their sprites
users = {}  # {sid: {"name": "User", "x": 100, "y": 100, "sprite": "rectangle"}}
screen_width, screen_height = 800, 600  # Game screen dimensions

@app.route("/")
def laptop_screen():
    return render_template("laptop.html")  # Page for the laptop screen

@app.route("/phone")
def phone_screen():
    return render_template("phone.html")  # Page for users' phones

@socketio.on("join_game")
def handle_join(data):
    #Handle a user joining the game.
    sid = request.sid
    name = data["name"]
    users[sid] = {
        "name": name,
        "x": random.randint(50, screen_width - 50),
        "y": random.randint(50, screen_height - 50),
        "sprite": "rectangle"  # Representing the player's sprite as a rectangle
    }
    emit("user_list", {"users": list(users.values())}, broadcast=True)
    emit("joined_ack", {"message": f"Welcome {name}!"}, room=sid)

@socketio.on("move_sprite")
def handle_move(data):
    #Handle sprite movement.
    sid = request.sid
    if sid in users:
        direction = data["direction"]
        if direction == "left":
            users[sid]["x"] -= 10
        elif direction == "right":
            users[sid]["x"] += 10
        elif direction == "up":
            users[sid]["y"] -= 10
        elif direction == "down":
            users[sid]["y"] += 10
        
        # Ensure the sprite stays within bounds
        users[sid]["x"] = max(0, min(users[sid]["x"], screen_width - 20))  # Width of sprite is 20px
        users[sid]["y"] = max(0, min(users[sid]["y"], screen_height - 20))  # Height of sprite is 20px
        
        # Emit to all clients to update the sprites
        emit("update_sprites", {"users": users}, broadcast=True)

@socketio.on("start_game")
def start_game():
    # Start the game, trigger the display of the game screen.
    emit("game_started", {"message": "The game has started!"}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


"""
"""
# Backend ussing Flask for server & flask_socketio for WebSockets
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
socketio = SocketIO(app)

# Get the laptop IP from the environment variable
laptop_ip = os.getenv('LAPTOP_IP', '127.0.0.1')  # Default to localhost if not set

# Route for the laptop main screen (game display)
@app.route('/laptop')
def laptop():
    return render_template('laptop.html', laptop_ip=laptop_ip)

# Route for the mobile controller interface
@app.route('/mobile')
def mobile():
    return render_template('mobile.html', laptop_ip=laptop_ip)

# WebSocket event to handle controller button presses
@socketio.on('button_pressed')
def handle_button_press(data):
    action = data.get('action')
    if action == 'start':
        emit('game_update', {'message': 'Game in Progress'}, broadcast=True)
    elif action == 'stop':
        emit('game_update', {'message': 'Game Ended'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
"""