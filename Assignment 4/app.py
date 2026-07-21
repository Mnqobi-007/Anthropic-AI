from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer  # ← ADD THIS
from pydantic import BaseModel, EmailStr
import sqlite3
from contextlib import contextmanager
from typing import Optional, List
from auth import create_user_jwt, get_current_user, signup_user, refresh_supabase_token, supabase

# Security scheme for Swagger
security = HTTPBearer()  

# Models
class TaskCreate(BaseModel):
    name: str
    description: str
    done: bool = False

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    done: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

app = FastAPI(
    title="Auth · Login & Protect API",
    description="A secure API with Supabase Authentication",
    version="1.0.0"
)

# Database context manager
@contextmanager
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            done BOOLEAN NOT NULL DEFAULT FALSE,
            user_id TEXT NOT NULL
        )
    """)
    conn.commit()

# ============ AUTH ENDPOINTS ============

@app.post("/auth/signup")
async def sign_user(request: SignUpRequest):
    """Register a new user account"""
    # ✅ 400 Validation
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    return signup_user(request.email, request.password)

@app.post("/auth/login")
async def login_user(request: LoginRequest):
    """Authenticate and receive access token"""
    # ✅ 400 Validation
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    return create_user_jwt(request.email, request.password)

@app.post("/auth/refresh")
async def refresh_token(request: RefreshRequest):
    """Get a new access token using refresh token"""
    if not request.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    return refresh_supabase_token(request.refresh_token)

@app.post("/auth/logout", dependencies=[Depends(security)])  
async def logout_user(current_user: dict = Depends(get_current_user)):
    """End the user's session"""
    try:
        # For stateless JWT, logout is client-side token discard
        return {
            "message": "Logged out successfully. Please discard your tokens on the client side.",
            "user_id": current_user.get("sub")
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

# ============ PUBLIC ENDPOINTS ============

@app.get("/public/info")
async def public_info():
    """Public information - no authentication required"""
    return {
        "message": "Welcome stranger! This info is public.",
        "status": "API is running",
        "version": "1.0.0"
    }

# ============ PROTECTED PROFILE ENDPOINT ============

@app.get("/protected/profile", dependencies=[Depends(security)])  
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get the authenticated user's profile information"""
    try:
        # Get fresh user data from Supabase
        response = supabase.auth.get_user(current_user.get("sub"))
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": response.user.created_at,
            "last_sign_in_at": response.user.last_sign_in_at,
            "user_metadata": response.user.user_metadata,
            "confirmed_at": response.user.confirmed_at
        }
    except Exception:
        # Fallback to JWT payload if Supabase call fails
        return {
            "user": {
                "id": current_user.get("sub"),
                "email": current_user.get("email"),
                "created_at": current_user.get("created_at")
            }
        }

# ============ PROTECTED TASK ENDPOINTS ============

@app.post("/tasks/", dependencies=[Depends(security)])  
async def add_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new task (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (name, description, done, user_id) VALUES (?, ?, ?, ?)",
            (task.name, task.description, task.done, current_user.get("sub"))
        )
        conn.commit()
        task_id = cursor.lastrowid
        return {
            "message": "Task added successfully",
            "task_id": task_id,
            "task": task
        }

@app.get("/tasks/", dependencies=[Depends(security)]) 
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for the authenticated user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (current_user.get("sub"),)
        )
        rows = cursor.fetchall()
        tasks = [dict(row) for row in rows]
        return {"tasks": tasks}

@app.get("/tasks/search/", dependencies=[Depends(security)])  
async def get_task_by_name(
    name: str,
    current_user: dict = Depends(get_current_user)
):
    """Search tasks by name (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE name LIKE ? AND user_id = ?",
            (f"%{name}%", current_user.get("sub"))
        )
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tasks found with that name"
            )
        tasks = [dict(row) for row in rows]
        return {"tasks": tasks}

@app.get("/tasks/filter", dependencies=[Depends(security)])  
async def get_filtered_tasks(
    done: bool,
    current_user: dict = Depends(get_current_user)
):
    """Filter tasks by completion status (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE done = ? AND user_id = ?",
            (done, current_user.get("sub"))
        )
        rows = cursor.fetchall()
        tasks = [dict(row) for row in rows]
        return {"tasks": tasks}

@app.get("/tasks/stats", dependencies=[Depends(security)]) 
async def get_task_stats(current_user: dict = Depends(get_current_user)):
    """Get task statistics (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
            (current_user.get("sub"),)
        )
        total = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE done = 1 AND user_id = ?",
            (current_user.get("sub"),)
        )
        completed = cursor.fetchone()[0]
        
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed
        }

@app.get("/tasks/{task_id}", dependencies=[Depends(security)]) 
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific task by ID (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return {"task": dict(row)}

@app.put("/tasks/{task_id}", dependencies=[Depends(security)]) 
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a task (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        updates = []
        params = []
        if task.name is not None:
            updates.append("name = ?")
            params.append(task.name)
        if task.description is not None:
            updates.append("description = ?")
            params.append(task.description)
        if task.done is not None:
            updates.append("done = ?")
            params.append(task.done)
        
        if updates:
            params.append(task_id)
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        updated_row = cursor.fetchone()
        return {
            "message": "Task updated successfully",
            "task": dict(updated_row)
        }

@app.put("/tasks/complete/{task_id}", dependencies=[Depends(security)]) 
async def complete_task(
    task_id: int,
    done: bool,
    current_user: dict = Depends(get_current_user)
):
    """Mark a task as complete/incomplete (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        cursor.execute(
            "UPDATE tasks SET done = ? WHERE id = ? AND user_id = ?",
            (done, task_id, current_user.get("sub"))
        )
        conn.commit()
        
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        updated_row = cursor.fetchone()
        return {
            "message": "Task updated successfully",
            "task": dict(updated_row)
        }

@app.delete("/tasks/{task_id}", dependencies=[Depends(security)]) 
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a task (authenticated)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.get("sub"))
        )
        conn.commit()
        return {
            "message": "Task deleted successfully",
            "task": dict(row)
        }