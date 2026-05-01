from fastapi import APIRouter, Depends, HTTPException
from app.models.idea_model import IdeaSubmission

router = APIRouter(
    prefix="/user-submissions",
    tags=["User Submissions"],
    responses={404: {"description": "Not found"}},
)
@router.post("api/generate")
async def generate_workflow(idea: IdeaSubmission):
    return {"message": f"Workflow generated for idea: {idea.idea}"}