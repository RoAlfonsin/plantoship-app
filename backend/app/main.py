from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db_utils import Database
from app.routers import user_submissions_routers
from app.llm_service import llm_service

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

app.include_router(user_submissions_routers.router)

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

@app.get("/llm-health")
async def llm_health_check():
    """Endpoint to check the health of the LLM service."""
    try:
        health_status = await llm_service.health_check()
        return health_status
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/llm-test")
async def llm_test(prompt: str = "Hello! Please respond with a brief greeting."):
    """Test endpoint to verify LLM service functionality."""
    try:
        response = await llm_service.generate_content(prompt)
        return {
            "success": True,
            "response": response["content"][:200],  # Truncate for display
            "metadata": {
                "attempt": response["attempt"],
                "finish_reason": response["finish_reason"]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# To run this locally (after activating venv): uvicorn main:app --reload