from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI(
    title="Monorepo Backend API",
    description="FastAPI service handling core business logic."
)

class Item(BaseModel):
    """Schema for incoming request data."""
    name: str
    description: str | None = None

@app.get("/")
async def read_root():
    return {"status": "Server running successfully", "service": "Backend"}

@app.get ("/health")
async def health_check():
    """Endpoint to check the health of the service."""
    return {"status": "healthy", "service": "Backend"}

@app.post("/items/")
async def create_item(item: Item):
    """Endpoint to demonstrate basic item creation."""
    return {"message": f"Item {item.name} created.", "data": item}

# To run this locally (after activating venv): uvicorn main:app --reload