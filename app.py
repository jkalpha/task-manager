"""
Project:   task-manager
File:      app.py
Author:    Josiah De Leon
Date:      2026-07-30

Description: application built to learn how apis work
"""

from collections import UserDict
import database as db
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def create_app(test_config=None) -> Flask: # App factory for dynamic sessions
    app = Flask(__name__)
    app.config.from_mapping({
        "DATABASE": "task_manager.db",
        "JWT_SECRET_KEY": "CA92FF703D1FDEA5-CA92FF703D1FDEA5"
        })
    jwt = JWTManager(app)
    
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


    @app.route("/tasks/<int:user_id>", methods=["GET"])
    def get_tasks_by_user(user_id: int):
        """Retrieves an existing cluster of tasks according to user_id.

        :param user_id: int, id associated with an existing user.
        :return: JSON of the full contents of tasks associated
            with the user_id, throws an error if there's no tasks
            associated with the user.
        """
        task = db.get_tasks_id(user_id)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Task not found"}), 404


    """
                    ~~POST~~
    """
    # TODO: Handle a missing title and duplicates
    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def add_task():
        """Adds a new task to the tasks table and assigns an id.

        :return: JSON of content for newly added task,
            thorws error if the task doesn't have a title.
        """
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}
        if "title" in data:
            new_task = {
                "user_id": user_id,
                "title": data["title"],
                "completed": False
            } 
            new_id = db.create_tasks(new_task)
            task = f"({new_id}).{new_task["title"]} was added."

            return jsonify({"status": task}), 201
        return jsonify({"error": "Malformed JSON"}), 400
    


    @app.route("/signup", methods=["POST"])
    def create_user():
        """Creates a new user with email and password.

        :return: JSON verifying that user was added successfully.
        """
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")
        
        if email and password:
            if db.get_user_by_email(email):
                return jsonify({"error": "Email already exits"}), 409
            password_hash = generate_password_hash(password)
            db.create_user(email=email, password_hash=password_hash)
            status = "user successfully created"
            return jsonify({"status": status}), 201
        return jsonify({"error": "Invalid operation"}), 400
    

    @app.route("/login", methods=["POST"])
    def login():
        """User login by username and password.

        :return: JSON with access token
        """
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Invalid request"}), 400

        user = db.get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            token = create_access_token(identity=str(user["id"]))
            return jsonify({"access_token": token}), 200

        return jsonify({"error": "Incorrect credentials"}), 401
        
    """
                    ~~PUT~~
    """

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    @jwt_required()
    def update_task(task_id: int):
        """Updates tasks according to id.

        *:param task_id: int, id associated with existing task.
        :return: JSON of the full content of task associated with the id
            if it exists else throw an error.
        """
        user_id = get_jwt_identity()
        data = request.get_json(silent=True) or {}

        if "completed" in data:
            parse_task = {
                "user_id": user_id,
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
    @jwt_required()
    def remove_task(task_id: int):
        """Removes a task from the tasks table in the database.

        :param task_id: int, id associate with existing task.
        :return: JSON verifying that the task was sucessfully
            removed. If tasks doesn't exist, throws an error.
        """
        user_id = get_jwt_identity()

        if db.remove_tasks(task_id=task_id, user_id=user_id):
            return "", 204
        return jsonify({"error": "Task not found"}), 404
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
