import pytest
from app.utils.prompt_builder import prompt_builder, validate_prompt_inputs


class TestPromptBuilder:
    """Test suite for the prompt_builder function"""
    
    def test_prompt_builder_success(self):
        """Test successful prompt generation with valid inputs"""
        idea = "Create a task management application with user authentication"
        stack = ["React", "FastAPI", "MongoDB"]
        
        result = prompt_builder(idea, stack)
        
        assert isinstance(result, str)
        assert "Create a task management application with user authentication" in result
        assert "The project MUST use React" in result
        assert "The project MUST use FastAPI" in result
        assert "The project MUST use MongoDB" in result
        assert "machine-readable format (JSON)" in result
        assert "project_summary" in result
        assert "development_steps" in result
    
    def test_prompt_builder_empty_idea(self):
        """Test prompt builder with empty idea"""
        idea = ""
        stack = ["React", "FastAPI"]
        
        with pytest.raises(ValueError, match="Invalid inputs: Validation failed: Idea cannot be empty"):
            prompt_builder(idea, stack)
    
    def test_prompt_builder_short_idea(self):
        """Test prompt builder with idea shorter than minimum length"""
        idea = "Short idea"
        stack = ["React", "FastAPI"]
        
        with pytest.raises(ValueError, match="Invalid inputs: Validation failed: Idea must be at least 20 characters long"):
            prompt_builder(idea, stack)
    
    def test_prompt_builder_empty_stack(self):
        """Test prompt builder with empty stack"""
        idea = "Create a web application for project management"
        stack = []
        
        with pytest.raises(ValueError, match="Invalid inputs: Validation failed: Stack must be a non-empty list"):
            prompt_builder(idea, stack)
    
    def test_prompt_builder_none_stack(self):
        """Test prompt builder with None stack"""
        idea = "Create a web application for project management"
        stack = None
        
        with pytest.raises(ValueError, match="Invalid inputs: Validation failed: Stack must be a non-empty list"):
            prompt_builder(idea, stack)
    
    def test_prompt_builder_invalid_stack_item(self):
        """Test prompt builder with invalid stack item"""
        idea = "Create a web application for project management"
        stack = ["React", "", "FastAPI"]
        
        with pytest.raises(ValueError, match="Invalid inputs: Validation failed: Technology at position 2 must be a non-empty string"):
            prompt_builder(idea, stack)
    
    def test_prompt_builder_single_tech_stack(self):
        """Test prompt builder with single technology"""
        idea = "Create a simple blog application"
        stack = ["React"]
        
        result = prompt_builder(idea, stack)
        
        assert "Create a simple blog application" in result
        assert "The project MUST use React" in result
        assert result.count("- The project MUST use") == 1
    
    def test_prompt_builder_large_stack(self):
        """Test prompt builder with multiple technologies"""
        idea = "Create an e-commerce platform"
        stack = ["React", "FastAPI", "MongoDB", "Redis", "Docker", "Nginx"]
        
        result = prompt_builder(idea, stack)
        
        assert "Create an e-commerce platform" in result
        assert "The project MUST use React" in result
        assert "The project MUST use FastAPI" in result
        assert "The project MUST use MongoDB" in result
        assert "The project MUST use Redis" in result
        assert "The project MUST use Docker" in result
        assert "The project MUST use Nginx" in result
        assert result.count("- The project MUST use") == 6
    
    def test_prompt_builder_whitespace_handling(self):
        """Test prompt builder handles whitespace properly"""
        idea = "  Create a todo app with extra spaces  "
        stack = ["  React  ", "  FastAPI  "]
        
        result = prompt_builder(idea, stack)
        
        assert "Create a todo app with extra spaces" in result
        assert "The project MUST use React" in result
        assert "The project MUST use FastAPI" in result
        assert "  Create a todo app with extra spaces  " not in result
        assert "  React  " not in result
    
    def test_prompt_builder_structure(self):
        """Test prompt builder has proper structure"""
        idea = "Create a social media dashboard"
        stack = ["React", "FastAPI", "PostgreSQL"]
        
        result = prompt_builder(idea, stack)
        
        # Check for required sections
        assert "## Project Idea" in result
        assert "## Technology Stack Constraints" in result
        assert "## Output Requirements" in result
        assert "## Instructions" in result
        
        # Check for JSON structure description
        assert '"project_summary"' in result
        assert '"architecture"' in result
        assert '"development_steps"' in result
        assert '"file_structure"' in result
        assert '"key_dependencies"' in result
        assert '"implementation_notes"' in result


class TestValidatePromptInputs:
    """Test suite for the validate_prompt_inputs function"""
    
    def test_validate_success(self):
        """Test successful validation"""
        idea = "Create a web application"
        stack = ["React", "FastAPI"]
        
        result = validate_prompt_inputs(idea, stack)
        
        assert result["status"] == "valid"
        assert result["idea"] == "Create a web application"
        assert result["stack"] == ["React", "FastAPI"]
    
    def test_validate_empty_idea(self):
        """Test validation with empty idea"""
        idea = ""
        stack = ["React", "FastAPI"]
        
        with pytest.raises(ValueError, match="Validation failed: Idea cannot be empty"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_short_idea(self):
        """Test validation with short idea"""
        idea = "Too short"
        stack = ["React", "FastAPI"]
        
        with pytest.raises(ValueError, match="Validation failed: Idea must be at least 20 characters long"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_empty_stack(self):
        """Test validation with empty stack"""
        idea = "Create a comprehensive web application"
        stack = []
        
        with pytest.raises(ValueError, match="Validation failed: Stack must be a non-empty list"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_none_stack(self):
        """Test validation with None stack"""
        idea = "Create a comprehensive web application"
        stack = None
        
        with pytest.raises(ValueError, match="Validation failed: Stack must be a non-empty list"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_invalid_stack_type(self):
        """Test validation with invalid stack type"""
        idea = "Create a comprehensive web application"
        stack = "React"  # String instead of list
        
        with pytest.raises(ValueError, match="Validation failed: Stack must be a non-empty list"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_empty_stack_item(self):
        """Test validation with empty stack item"""
        idea = "Create a comprehensive web application"
        stack = ["React", "", "FastAPI"]
        
        with pytest.raises(ValueError, match="Validation failed: Technology at position 2 must be a non-empty string"):
            validate_prompt_inputs(idea, stack)
    
    def test_validate_whitespace_cleaning(self):
        """Test validation cleans whitespace properly"""
        idea = "  Create a web application  "
        stack = ["  React  ", "  FastAPI  "]
        
        result = validate_prompt_inputs(idea, stack)
        
        assert result["status"] == "valid"
        assert result["idea"] == "Create a web application"
        assert result["stack"] == ["React", "FastAPI"]
