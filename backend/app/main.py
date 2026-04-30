from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .utils.db_utils import Database

# Initialize FastAPI application
app = FastAPI(
    title="Monorepo Backend API",
    description="FastAPI service handling core business logic."
)

# Allowed origins
origins = [
    "http://localhost:5173",  # Frontend running on port 3000
]

# Configure and apply Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Which origins can access the API
    allow_credentials=True,       # Allows passing cookies/session data
    allow_methods=["*"],          # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allows all headers
)

db = Database()

@app.get("/")
async def read_root():
    return {"status": "Server running successfully", "service": "Backend"}

@app.get ("/health")
async def health_check():
    """Endpoint to check the health of the service."""
    return {"status": "healthy", "service": "Backend"}

@app.get("/db-test")
async def db_test():
    success, message = await db.test_connection()
    return {"success": success, "message": message}

# To run this locally (after activating venv): uvicorn main:app --reload