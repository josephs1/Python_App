from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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
    global player  # Reference the global player dictionary
    direction = data["direction"]
    speed = data.get("speed", 10)  # Default speed if not provided

    # Move player based on direction
    if direction == "up":
        player["y"] -= speed
    elif direction == "down":
        player["y"] += speed
    elif direction == "left":
        player["x"] -= speed
    elif direction == "right":
        player["x"] += speed

    # Broadcast the new player position
    emit("update_position", {"x": player["x"], "y": player["y"]}, broadcast=True)

@socketio.on("stop_player")
def handle_stop():
    # Optionally handle stopping movement if needed
    pass

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
