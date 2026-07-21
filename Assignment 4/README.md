# Auth · Login & Protect

A secure REST API with Supabase Authentication - sign up, log in, log out, and protect routes with JWT verification.

## 🚀 Features

- User registration (Sign Up)
- User authentication (Login) with JWT
- Token refresh
- Protected routes with middleware
- SQLite database with user-specific tasks
- Swagger UI documentation with Bearer auth
- Comprehensive error handling

## 📋 API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/signup` | ❌ | Register a new user |
| POST | `/auth/login` | ❌ | Login and get tokens |
| POST | `/auth/refresh` | ❌ | Refresh access token |
| POST | `/auth/logout` | ✅ | End session |
| GET | `/public/info` | ❌ | Public information |
| POST | `/tasks/` | ✅ | Create a task |
| GET | `/tasks/` | ✅ | Get all tasks |
| GET | `/tasks/search/` | ✅ | Search tasks by name |
| GET | `/tasks/filter` | ✅ | Filter tasks by status |
| GET | `/tasks/stats` | ✅ | Get task statistics |
| GET | `/tasks/{id}` | ✅ | Get specific task |
| PUT | `/tasks/{id}` | ✅ | Update a task |
| PUT | `/tasks/complete/{id}` | ✅ | Toggle task completion |
| DELETE | `/tasks/{id}` | ✅ | Delete a task |

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Auth**: Supabase Auth (JWT)
- **Database**: SQLite
- **Language**: Python 3.10+
