"""
Project:   task-manager
File:      app.py
Author:    Josiah De Leon
Date:      2026-07-30

Description: application built to learn how apis work
"""
import database as db

from flask import Flask, jsonify, request
app = Flask(__name__)


# Non persistent task list used to test CRUD
# tasks = [
#         {"id": 1, "title": "workout", "completed": False},
#         {"id": 2, "title": "study", "completed": False},
#         {"id": 3, "title": "budget", "completed": True},
#         {"id": 4, "title": "email Sara", "completed": False},
#         {"id": 5, "title": "work on mle unit 9", "completed": False},
#         {"id": 6, "title": "java 1", "completed": False}
#     ]


"""
                ~~GET~~
"""
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
    """
    Retrieves all tasks.

    Args: None

    Returns: All tasks
    """
    return jsonify(db.get_tasks_all())


# TODO: Implement with db and include user
@app.route("/tasks/<int:task_id>", methods=["GET"])
def tasks_by_id(task_id: int):
    """
    Retrieves an exixting task according to it's id

    Args: task_id: int - id associated with existing task

    Returns: JSON of the full contents of task associated
             with the id and throws an error if the task
             doesn't exist
    """
    task = db.get_tasks_id(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


"""
                ~~POST~~
"""
# TODO: Handle a missing title and duplicates
@app.route("/tasks", methods=["POST"])
def AddTasks():
    """
    Adds a new task to the list and assigns an id.

    Args: None

    Returns: JSON of content for newly added task and
             thorws an error if the task doesn't have
             a title
    """
    data = request.get_json()
    if "title" in data:
        new_task = {
        "title": data["title"],
        "completed": False
    }
        new_id = db.create_tasks(new_task)
        new_task["id"] = new_id
        return jsonify(new_task), 201
    return jsonify({"error": "Task need 'title'"}), 404


"""
                ~~PUT~~
"""
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def UpdateTask(task_id):
    """
    This funciton updates tasks according to id.

    Args: task_id: int - id associated with existing task

    Returns: JSON of the full content of task associated with the id
             if it exists else throw an error
    """
    data = request.get_json()

    if "completed" in data:
        parse_task = {
            "id": task_id,
            "completed": data["completed"]
        }
        db.update_completion(parse_task)
        return jsonify(parse_task), 200

    return jsonify({"error": "Task not found"}), 404

"""
                ~~DELETE~~
"""
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def RemoveTask(task_id: int):
    """
    Removes a task from the list

    Args: task_id: int - id associate with existing task
    
    Returns: JSON verifying that the task was sucessfully
             removed. If tasks doesn't exist, throws an
             error
    """
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            status = f"{task["title"]} was removed."
            tasks.pop()
            # Explore 204 No content
            return jsonify(status), 200
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
