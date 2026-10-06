# Ibhotwe Backend

This folder contains the server-side code and REST API for the WSU Ibhotwe Food Ordering Platform.

## Structure
- **`main.py`** — FastAPI application, API endpoints, role-based authentication, and SQLite database operations.
- **`requirements.txt`** — Python dependencies required by the backend (`fastapi`, `uvicorn`, `pydantic[email]`).

## Running the Backend
From this folder:
```powershell
py -m uvicorn main:app --reload
```
Or from the project root:
```powershell
py -m uvicorn backend.main:app --reload
```

