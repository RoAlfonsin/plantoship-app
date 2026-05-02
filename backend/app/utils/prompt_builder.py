from typing import List, Dict, Any
from app.models.idea_model import IdeaSubmission

def check_idea_builder(idea: IdeaSubmission) -> str:
    return f""" 
      Idea: {idea.idea},
      Frontend: {idea.stack['frontend']},
      Backend: {idea.stack['backend']},
      Database: {idea.stack['database']},
      Deployment: {idea.stack['deployment']},
      is this enough information to generate a workflow for a new web app project? Answer yes or no."""

def prompt_builder(idea: str, stack: List[str]) -> str:
    """
    Creates a structured prompt for LLM based on project idea and technology stack.
    
    Args:
        idea: Project description string
        stack: List of selected technologies
        
    Returns:
        Formatted prompt string for LLM
        
    Raises:
        ValueError: For invalid inputs
    """
    # Validate inputs using existing validation function
    try:
        validation_result = validate_prompt_inputs(idea, stack)
        validated_idea = validation_result["idea"]
        validated_stack = validation_result["stack"]
    except ValueError as e:
        raise ValueError(f"Invalid inputs: {str(e)}")
    
    # Build the prompt with structured sections
    prompt = f"""You are an expert software architect and developer. Based on the following project requirements, generate a comprehensive development workflow and implementation plan.

## Project Idea
{validated_idea}

## Technology Stack Constraints
The project MUST use the following technologies:
"""
    
    # Add each technology as a constraint
    for tech in validated_stack:
        prompt += f"- The project MUST use {tech}\n"
    
    prompt += f"""

## Output Requirements
Your output MUST be in a machine-readable format (JSON) with the following structure:
{{
  "project_summary": "Brief description of the project",
  "architecture": "High-level architecture overview",
  "development_steps": [
    {{"step": 1, "description": "Step description", "estimated_hours": "number"}},
    {{"step": 2, "description": "Step description", "estimated_hours": "number"}}
  ],
  "file_structure": "Recommended file/folder structure",
  "key_dependencies": ["dependency1", "dependency2"],
  "implementation_notes": "Additional technical considerations"
}}

## Instructions
1. Analyze the project idea thoroughly
2. Design an appropriate architecture using the specified technology stack
3. Create a step-by-step development workflow
4. Provide practical implementation guidance
5. Ensure all recommendations align with the required technologies
6. Output your response in the exact JSON format specified above

Generate the complete development plan now."""
    
    return prompt

def create_idea_validation_prompt(idea: str, stack: Dict[str, str]) -> str:
    """
    Creates a prompt for LLM to validate if the provided idea and stack are sufficient 
    for generating a comprehensive development workflow.
    
    Args:
        idea: Project description string
        stack: Dictionary of technology categories and their choices
        
    Returns:
        Formatted prompt string for LLM validation
    """
    # Format the stack information
    stack_info = "\n".join([f"- {category}: {tech}" for category, tech in stack.items()])
    
    prompt = f"""You are an experienced programming instructor and mentor helping students create impressive portfolio projects.

I need you to evaluate if the following project information is sufficient to generate a comprehensive learning workflow with 15-30 highly detailed issues/steps that will help the student build a complete portfolio-worthy application.

## Project Idea:
{idea}

## Technology Stack:
{stack_info}

## Evaluation Criteria:
Please assess if we have enough information to create a detailed development plan that includes:
1. Project architecture and design patterns
2. Step-by-step development workflow
3. File structure and organization
4. Key dependencies and setup requirements
5. Implementation best practices
6. Testing strategy
7. Deployment considerations

## Response Format:
Respond with ONLY "yes" or "no" (lowercase, no punctuation):

- "yes" if the information is sufficient to generate a comprehensive 15-30 step workflow
- "no" if more specific details are needed about the project requirements, features, or learning objectives

## Decision Guidelines:
Consider the information sufficient if:
- The project idea clearly describes what to build
- The technology stack is complete and compatible
- The scope is reasonably defined for a web application

Consider more information needed if:
- The project idea is too vague or unclear
- Key features or functionality are not specified
- The scope is ambiguous (e.g., "build a social media app" without details)
- Critical requirements are missing

Based on the above information, is this sufficient to proceed with workflow generation?"""

    return prompt

def validate_prompt_inputs(idea: str, stack: List[str]) -> Dict[str, Any]:
    """
    Validates inputs for prompt generation without technology constraints.
    
    Args:
        idea: Project description string
        stack: List of selected technologies (any values allowed)
        
    Returns:
        Dict with validation status and cleaned inputs
        
    Raises:
        ValueError: For invalid inputs
    """
    errors = []
    
    # Validate idea
    if not idea or not idea.strip():
        errors.append("Idea cannot be empty")
    elif len(idea.strip()) < 20:
        errors.append("Idea must be at least 20 characters long")
    
    # Validate stack structure (but not content)
    if not stack or not isinstance(stack, list):
        errors.append("Stack must be a non-empty list")
    elif len(stack) < 1:
        errors.append("At least one technology must be selected")
    
    # Validate stack items are strings
    if isinstance(stack, list):
        for i, tech in enumerate(stack):
            if not isinstance(tech, str) or not tech.strip():
                errors.append(f"Technology at position {i+1} must be a non-empty string")
    
    if errors:
        raise ValueError(f"Validation failed: {'; '.join(errors)}")
    
    # Clean and return inputs
    cleaned_stack = [tech.strip() for tech in stack if tech.strip()]
    return {"status": "valid", "idea": idea.strip(), "stack": cleaned_stack}