from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.utils.prompt_builder import prompt_builder, create_idea_validation_prompt

router = APIRouter(
    prefix="/user-submissions",
    tags=["User Submissions"],
    responses={404: {"description": "Not found"}},
)

class PromptBuilderRequest(BaseModel):
    idea: str = Field(..., description="Project idea description", min_length=20)
    stack: List[str] = Field(..., description="List of technologies to use", min_items=1)

class PromptBuilderResponse(BaseModel):
    prompt: str = Field(..., description="Generated prompt for LLM")
    success: bool = Field(..., description="Whether prompt generation was successful")
    message: str = Field(..., description="Status message")

class CheckIdeaRequest(BaseModel):
    idea: str = Field(..., description="Project idea description")
    stack: Dict[str, str] = Field(..., description="Technology stack with categories")

class CheckIdeaResponse(BaseModel):
    sufficient: bool = Field(..., description="Whether the information is sufficient")
    prompt: str = Field(..., description="Prompt sent to LLM")
    response: str = Field(..., description="LLM response")
    message: str = Field(..., description="Status message")

@router.post("/api/generate")
async def generate_workflow(idea):
    return {"message": f"Workflow generated for idea: {idea}"}

@router.post("/api/check-idea", response_model=CheckIdeaResponse)
async def check_idea(request: CheckIdeaRequest):
    """
    Validates if the provided idea and stack are sufficient for workflow generation.
    Creates a prompt for LLM to evaluate the information.
    """
    try:
        # Create the validation prompt for LLM
        validation_prompt = create_idea_validation_prompt(request.idea, request.stack)
        
        # TODO: Integrate with actual LLM service (Gemini 2.0 Flash)
        # For now, we'll simulate a basic validation based on idea length and stack completeness
        is_sufficient = len(request.idea.strip()) >= 10 and len(request.stack) >= 3
        
        # Simulated LLM response (replace with actual LLM call)
        llm_response = "yes" if is_sufficient else "no"
        
        return CheckIdeaResponse(
            sufficient=is_sufficient,
            prompt=validation_prompt,
            response=llm_response,
            message="Idea validation completed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/api/prompt-builder", response_model=PromptBuilderResponse)
async def create_prompt(request: PromptBuilderRequest):
    """
    Generate a structured prompt for LLM based on project idea and technology stack.
    """
    try:
        generated_prompt = prompt_builder(request.idea, request.stack)
        return PromptBuilderResponse(
            prompt=generated_prompt,
            success=True,
            message="Prompt generated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )