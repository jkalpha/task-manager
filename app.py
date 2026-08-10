"""
Project:   task-manager
File:      app.py
Author:    Josiah De Leon
Date:      2026-07-30

Description: application built to learn how apis work
"""
# TODO: Update Docstring for db and not list
import database as db

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash

def create_app(test_config=None) -> Flask: # App factory for dynamic sessions
    app = Flask(__name__)
    app.config.from_mapping({"DATABASE": "task_manager.db"})
    
    if test_config:
        app.config.update(test_config)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #             NON-PERSISTENT IMPLEMENTATION FOR INITIAL CRUD            #
    # tasks = [                                                             #
    #         {"id": 1, "title": "workout", "completed": False},            #
    #         {"id": 2, "title": "study", "completed": False},              #
    #         {"id": 3, "title": "budget", "completed": True},              #
    #         {"id": 4, "title": "email Sara", "completed": False},         #
    #         {"id": 5, "title": "work on mle unit 9", "completed": False}, #
    #         {"id": 6, "title": "java 1", "completed": False}              #
    #     ]                                                                 #
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    """
                    ~~GET~~
    """
    @app.route("/health", methods=["GET"])
    def health_status():
        """Checks the health of the API connection.

        :param "/health": Directory path in the site folder.
        :param methods: (optional)["GET"], HTTP method used to retrieve resources from the server.
        :return: JSON of the status with 200 code "successful".
        """
        return jsonify({"status": "ok"}), 200


    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        """Retrieves all tasks.

        :return: All tasks stored in database.
        """
        return jsonify(db.get_tasks_all())


    # TODO: Implement using user_id
    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_tasks_by_id(task_id: int):
        """Retrieves an exixting task according to it's id (TASK TABLE).

        :param task_id: int, id associated with existing task.
        :return: JSON of the full contents of task associated
            with the id and throws an error if the task doesn't
            exist.
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
    def add_task():
        """Adds a new task to the tasks table and assigns an id.

        :return: JSON of content for newly added task,
            thorws error if the task doesn't have a title.
        """
        data = request.get_json(silent=True) or {}
        if "title" in data:
            new_task = {
            "title": data["title"],
            "completed": False
        }
            new_id = db.create_tasks(new_task)
            new_task["id"] = new_id
            return jsonify(new_task), 201
        return jsonify({"error": "Task need 'title'"}), 400
    
    @app.route("/signup", methods=["POST"])
    def create_user():
        """Creates a new user with email and password.

        :return: JSON verifiying that user was added successfully.
        """
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = str(data.get("password"))
        
        if email and password:
            password_hash = generate_password_hash(password)
            # TODO: Check if the email already exists
            # test with: c.post("/signup", json={"email": "a@b.com", "password": "hunter2"})
            db.create_user(email=email, password_hash=password_hash)
            status = "user successfully created"
            return jsonify(status), 201
        return jsonify({"error": "Invalid operation"}), 400

    """
                    ~~PUT~~
    """
    # TODO: 
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        """Updates tasks according to id.

        :param task_id: int, id associated with existing task.
        :return: JSON of the full content of task associated with the id
            if it exists else throw an error.
        """
        data = request.get_json(silent=True) or {}

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
    def remove_task(task_id: int):
        """Removes a task from the tasks table in the database.

        :param task_id: int, id associate with existing task.
        :return: JSON verifying that the task was sucessfully
            removed. If tasks doesn't exist, throws an error.
        """
        if db.remove_tasks(task_id):
            return "", 204
        return jsonify({"error": "Task not found"}), 404
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
