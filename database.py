import sqlite3 as sqweel
from app import tasks

connection = sqweel.connect("task_manager.db")

try:
    cursor = connection.cursor()

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
    connection.commit()

except sqweel.Error as error:
    print(f"An error occured: {error}")

finally:
    connection.close()
