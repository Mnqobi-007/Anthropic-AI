from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3   # sqlite3 for my database storage

class Task(BaseModel):
    name: str
    description: str
    done: bool

app = FastAPI(
    title="Simple CRUD API",
    description="A simple CRUD API for managing tasks",
    version="1.0.0"
)

conn = sqlite3.connect("tasks.db")  # create / connect to db
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        done BOOLEAN NOT NULL DEFAULT FALSE,
    )
""")
conn.commit()

@app.post("/tasks/")
async def add_task(task: Task):
    cursor.execute("INSERT INTO tasks (name, description) VALUES (?, ?)", (task.name, task.description))
    conn.commit()
    return {"message": "Task added successfully", "task": task}

@app.get("/tasks/")
async def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()  # retrieve all tasks as a list
    tasks = [{"id": row[0], "name": row[1], "description": row[2], "done": row[3]} for row in rows]
    return {"tasks": tasks}

@app.get("/tasks/")  # get task by name (search task)
async def get_task_by_name(name: str):
    cursor.execute("SELECT * FROM tasks WHERE name LIKE ?", (name))
    row = cursor.fetchone()
    if not row:
        return {"error": "Task not found"}
    return {"task": {"id": row[0], "name": row[1], "description": row[2], "done": row[3]}}

@app.get("/tasks") # get complete or incomplete tasks
async def get_completed_tasks(done: bool):
    cursor.execute("SELECT * FROM tasks WHERE done = ?", (done))
    rows = cursor.fetchall()
    tasks = [{"id": row[0], "name": row[1], "description": row[2], "done": row[3]} for row in rows]
    return {"tasks": tasks}

@app.get("/tasks/stats")  # count complete
async def get_completed_tasks():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = true")
    complete = cursor.fetchall()
    return {"rows": rows, "completed": complete}

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Task not found"}
    return {"task": {"id": row[0], "name": row[1], "description": row[2], "done": row[3]}}

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Task not found"}
    cursor.execute("UPDATE tasks SET name = ?, description = ?, done = ? WHERE id = ?", (task.name, task.description, task.done, task_id))
    conn.commit()
    return {"message": "Task updated successfully", "task": task}

# set complete
@app.put("/tasks/complete/{task_id}")
async def complete_task(task_id: int, task: Task):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Task not found"}
    cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (task.done, task_id))
    conn.commit()
    return {"message": "Task completed successfully", "task": task}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Task not found"}
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return {"message": "Task deleted successfully", "task": {"id": row[0], "name": row[1], "description": row[2]}}
