import sqlite3 as sqweel
# from werkzeug.security import generate_password_hash, check_password_hash
#from app import tasks

DB_PATH = "task_manager.db"

def connect_db():
    """Helper function that opens the database connection."""
    # PRAGMA foreign_keys = ON
    conn = sqweel.connect("task_manager.db") 
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_db() -> None:
    """Initializes schema with tasks and user tables.
    
    :return: Tasks and User tables.
    """
    conn = connect_db()
    try:
        cursor = conn.cursor()
        # Create tasks table        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR (50),
                completed BIT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )
        """)

        # Creates index for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)")

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR NOT NULL UNIQUE,
                password_hash VARCHAR NOT NULL
            )
        """)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #            IMPORTING DATA INTO TABLES TO ADD PERSISTANCE            #
        # for task in tasks:                                                  #
        #     cursor.execute(                                                 #
        #         "INSERT INTO tasks (id, title, completed) VALUES(?, ?, ?)", #
        #         (task["id"], task["title"], int(task["completed"]))         #
        #     )                                                               #
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        conn.commit()

    except sqweel.Error as error:
        print(f"An error occured: {error}")

    finally:
        conn.close()

def get_tasks_all() -> list:
    """Retrieves all tasks from the database.
    
    :return: List of dictionaries containing contents of tasks.
    """
    with connect_db() as conn:
        conn.row_factory = sqweel.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

    return [dict(row) for row in rows ]

def get_tasks_id(user_id: int) -> list:
    """Retrieves tasks by id from the tasks table.

    :param task_id: int, id associated with tasks.
    :return: List of dictionaries containing contents of tasks by id.
    """
    conn = connect_db()
    conn.row_factory = sqweel.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_tasks(new_task: dict):
    """Inserts a new row in Tasks.

    :param new_task: Dictonary, contains attibutes to be inserted.
    :return: int, ID associated with the newly created task.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute( 
     "INSERT INTO tasks (user_id, title, completed) VALUES (?,?,?)",
     (new_task["user_id"], new_task["title"], new_task["completed"]) 
     )

    conn.commit()
    print(f"{new_task["title"]} was added")
    conn.close()
    return cursor.lastrowid

def update_completion(task: dict):
    """Updates the status of existing task.

    :param task: Dictionary, contains attributes of task.
    :return: Print statement confirming operation was successful.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ? AND user_id = ?",
        ((1 if task["completed"] else 0), task["id"], task["user_id"])
    )

    conn.commit()
    conn.close()


def remove_tasks(task_id: int):
    """Removes a task from Tasks table.

    :param task_id: int, id associated with task.
    :return: int, row count to confirm that task was removed.
    """
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
        
    except sqweel.Error as error:
        print(f"An error occured: {error}" )
    
    finally:
        conn.close()

def create_user(email, password_hash) -> None:
    """Create a new user.
    
    :param email: str, email address of the new user.
    :param password_hash: str, hashed passowrd of user.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(email, password_hash) VALUES(?,?)",
        (email, password_hash)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email):
    """Checks if a user already exists by email.

    :param email: str, email address of the user.
    :return: dict, user information if user exists else none.
    """
    conn = connect_db()
    conn.row_factory = sqweel.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None

if __name__ == "__main__":
    initialize_db()
