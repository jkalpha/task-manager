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
def health_status():
    return jsonify({"status": "ok"}, 200)

if __name__ == "__main__":
    app.run(debug=True)
