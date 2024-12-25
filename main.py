from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import base64
import io
import time

app = Flask(__name__)
socketio = SocketIO(app)

is_streaming = False  # Variable para controlar la transmisión


@socketio.on("toggle_stream")
def toggle_stream(data):
    global is_streaming
    is_streaming = data["is_streaming"]
    if is_streaming:
        socketio.start_background_task(capture_and_send_screen)


def capture_and_send_screen():
    """Captura y envía imágenes mientras 'is_streaming' sea True."""
    global is_streaming
    while is_streaming:
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG", quality=50)
        encoded_image = base64.b64encode(buffer.getvalue()).decode()
        socketio.emit("screen_update", {"image": encoded_image})
        time.sleep(0.2)


@app.route("/view")
def view():
    # """Ruta para los músicos (solo visualización)."""
    return render_template("view.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
