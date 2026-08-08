import sqlite3 as sqweel
#from app import tasks

DB_PATH = "task_manager.db"

def connect_db():
    """Helper function that opens the database connection."""
    return sqweel.connect("task_manager.db")

def initialize_db() -> None:
    """Initializes schema with tasks and user tables."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        # Create tasks table        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR (50),
                completed BIT
            )
        """)
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR (60)    
            )
        """)

        # Importing data into tables to add persistence:
        # for task in tasks:
        #     cursor.execute(
        #         "INSERT INTO tasks (id, title, completed) VALUES(?, ?, ?)",
        #         (task["id"], task["title"], int(task["completed"]))
        #     )
        
        # 
        conn.commit()

    except sqweel.Error as error:
        print(f"An error occured: {error}")

    finally:
        conn.close()

def get_tasks_all() -> list:
    """Retrieves all tasks from the database."""
    with connect_db() as conn:
        conn.row_factory = sqweel.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

    return [dict(row) for row in rows ]

def get_tasks_id(id: int) -> list:
    """
    Retrieves tasks by id from the tasks table.

    Args: id: int - id associated with tasks

    Returns: list of dictionaries containing rows with attribute name keys and
             instance value pairs.
    """
    with connect_db() as conn:
        conn.row_factory = sqweel.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))

        rows = cursor.fetchall()
    return [dict(row) for row in rows]

def create_tasks(new_task: dict):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute( 
     "INSERT INTO tasks (title, completed) VALUES (?,?)",
     (new_task["title"], new_task["completed"]) 
     )

    conn.commit()
    print(f"{new_task["title"]} was added")
    conn.close()
    return cursor.lastrowid

if __name__ == "__main__":
    initialize_db()
