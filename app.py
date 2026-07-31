"""
Project:   task-manager
File:      app.py
Author:    Josiah De Leon
Date:      2026-07-30

Description: application built to learn how apis work
"""

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def HealthStatus():
    """
    Checks the health of the api connection.

    Args: 
        "/health" - Directory path in the site folder.
        methods=["GET"] - HTTP method used to retrieve resources from the server

    Returns: JSON of the status with 200 code "successful"

    """
    return jsonify({"status": "ok"}, 200)

if __name__ == "__main__":
    app.run(debug=True)
