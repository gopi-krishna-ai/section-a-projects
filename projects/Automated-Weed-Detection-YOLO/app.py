"""
Automated Weed Detection System Using YOLO
Flask web application entry point.
"""

import os
import socket

from flask import Flask, jsonify, render_template, request

from utils.detector import detect

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload cap

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect_route():
    if "image" not in request.files:
        return jsonify({"error": "Please choose an image to upload."}), 400

    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "Please choose an image to upload."}), 400
    if not _allowed(file.filename):
        return jsonify({"error": "Only JPG and PNG images are supported."}), 400

    try:
        result = detect(file.read())
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result)


def find_free_port(preferred, attempts=20):
    """First genuinely usable port at or after `preferred`.

    A killed server can leave a stale LISTENING socket on Windows that accepts
    connections then resets them, which the browser reports as "could not reach
    the server". Probing with a real connect() skips those dead sockets.
    """
    for port in range(preferred, preferred + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.4)
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder:
                binder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                binder.bind(("127.0.0.1", port))
            return port
        except OSError:
            continue
    raise RuntimeError(f"No free port in range {preferred}-{preferred + attempts}.")


if __name__ == "__main__":
    chosen = find_free_port(int(os.environ.get("PORT", 5100)))
    print("\n" + "=" * 62)
    print("  Automated Weed Detection System Using YOLO")
    print(f"  Open this in your browser:  http://127.0.0.1:{chosen}/")
    print("=" * 62 + "\n")
    # use_reloader=False is essential here: the reloader watches imported
    # modules, and torch/ultralytics touch files under site-packages at import
    # time. That was restarting the server mid-upload and resetting the
    # connection, so every detection request failed.
    app.run(debug=True, port=chosen, use_reloader=False)
