"""
run.py — Application entry point.

Run with:
    python run.py                         # Development
    gunicorn -w 4 -b 0.0.0.0:5000 run:app  # Production
"""

import os
from app import app
from database import init_db

# Select environment from ENV variable (default: development)
env = os.environ.get("FLASK_ENV", "development")

if __name__ == "__main__":
    with app.app_context():
        init_db(app)

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5000))
    debug = env == "development"

    print(f"""
╔══════════════════════════════════════════════════════════╗
║        🧠 Smart Study Planner AI — Backend Server       ║
╠══════════════════════════════════════════════════════════╣
║  Environment : {env:<42}║
║  Host        : {host:<42}║
║  Port        : {port:<42}║
║  Debug       : {str(debug):<42}║
╠══════════════════════════════════════════════════════════╣
║  API Base    : http://localhost:{port}/api               ║
║  Health      : http://localhost:{port}/api/health        ║
╚══════════════════════════════════════════════════════════╝
    """)

    app.run(host=host, port=port, debug=debug)
