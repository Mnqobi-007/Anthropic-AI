from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3   # sqlite3 for my database storage

class Item(BaseModel):
    name: str
    description: str

app = FastAPI(
    title="Simple CRUD API",
    description="A simple CRUD API for managing items",
    version="1.0.0"
)

conn = sqlite3.connect("items.db")  # create / connect to db
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
""")
conn.commit()

@app.post("/items/")
async def add_item(item: Item):
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (item.name, item.description))
    conn.commit()
    return {"message": "Item added successfully", "item": item}

@app.get("/items/")
async def get_items():
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    items = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
    return {"items": items}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Item not found"}
    return {"item": {"id": row[0], "name": row[1], "description": row[2]}}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Item not found"}
    cursor.execute("UPDATE items SET name = ?, description = ? WHERE id = ?", (item.name, item.description, item_id))
    conn.commit()
    return {"message": "Item updated successfully", "item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Item not found"}
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted successfully", "item": {"id": row[0], "name": row[1], "description": row[2]}}