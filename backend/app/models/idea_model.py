from pydantic import BaseModel, Field

class IdeaSubmission(BaseModel):
    idea: str = Field(..., des = "User's project idea", min_length=20)