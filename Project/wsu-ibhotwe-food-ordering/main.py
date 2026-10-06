"""
Ibhotwe Campus Food Ordering Platform
Root Entrypoint — forwards to backend/main.py
"""
import sys
from pathlib import Path

# Add backend directory to sys.path
_ROOT = Path(__file__).resolve().parent
_BACKEND = _ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from backend.main import app, init_db, db  # noqa: F401, E402

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
