from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str

app = FastAPI(
    title="Simple CRUD API",
    description="A simple CRUD API for managing items",
    version="1.0.0"
)

items = []

@app.post("/items/")
async def add_item(item: Item):
    items.append(item)
    return {"message": "Item added successfully", "item": item}

@app.get("/items/")
async def get_items():
    return {"items": items}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        return {"error": "Item not found"}
    return {"item": items[item_id]}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        return {"error": "Item not found"}
    items[item_id] = item
    return {"message": "Item updated successfully", "item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        return {"error": "Item not found"}
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}