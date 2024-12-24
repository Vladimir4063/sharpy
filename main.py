from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyautogui
import base64
import io
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return render_template("index.html")  # Archivo HTML que mostrará la pantalla


def capture_and_send_screen():
    """Captura la pantalla y la envía a los clientes conectados"""
    while True:
        print("ENTRE AL BUCLE")
        # Capturar pantalla
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG", quality=50)  # Comprimir captura
        encoded_image = base64.b64encode(buffer.getvalue()).decode()
        # Enviar captura a los clientes
        socketio.emit("screen_update", {"image": encoded_image})
        time.sleep(0.1)  # Control de frecuencia (10 FPS)


@socketio.on("connect")
def on_connect():
    print("Cliente conectado")


if __name__ == "__main__":
    # Ejecutar captura en un hilo separado
    Thread(target=capture_and_send_screen, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)
