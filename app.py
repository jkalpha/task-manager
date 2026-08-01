"""
Project:   task-manager
File:      app.py
Author:    Josiah De Leon
Date:      2026-07-30

Description: application built to learn how apis work
"""

from flask import Flask, jsonify, request
app = Flask(__name__)

tasks = [
        {"id": 1, "title": "workout", "completed": False},
        {"id": 2, "title": "study", "completed": False},
        {"id": 3, "title": "budget", "completed": True},
        {"id": 4, "title": "email Sara", "completed": False},
        {"id": 5, "title": "work on mle unit 9", "completed": False},
        {"id": 6, "title": "java 1", "completed": False}
    ]

@app.route("/health", methods=["GET"])
def HealthStatus():
    """
    Checks the health of the api connection.

    Args: 
        "/health" - Directory path in the site folder.
        methods=["GET"] - HTTP method used to retrieve resources from the server

    Returns: JSON of the status with 200 code "successful"

    """
    return jsonify({"status": "ok"}), 200

@app.route("/tasks", methods=["GET"])
def GetTasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def AddTasks():
    data = request.get_json()
    new_task = {
        "id": int(tasks[-1].get("id", 0) + 1),
        "title": data["title"],
        "completed": False
    }
    tasks.append(new_task)

    return jsonify(new_task), 201

# TODO: Implement GET /tasks by id
# TODO: Implement PUT /tasks
# TODO: Implement DELETE /tasks


if __name__ == "__main__":
    app.run(debug=True)

"""
-add sections to implement from chat
-commit
"""