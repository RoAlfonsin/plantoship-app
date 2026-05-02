import os
import time
import asyncio
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Service layer for handling Gemini LLM API interactions with retry logic and error handling."""
    
    def __init__(self):
        """Initialize the LLM service with API key and model configuration."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite-preview",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        # Retry configuration
        self.max_retries = 3
        self.base_delay = 1.0  # Base delay in seconds
        self.max_delay = 60.0  # Maximum delay in seconds
    
    def _exponential_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        # Add jitter to prevent thundering herd
        jitter = delay * 0.1 * (0.5 + (hash(time.time()) % 100) / 100)
        return delay + jitter
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """Determine if an error is retryable."""
        if isinstance(error, google_exceptions.GoogleAPICallError):
            # Retry on rate limit, server errors, and network issues
            return any(
                phrase in str(error).lower() 
                for phrase in ["rate limit", "quota", "timeout", "connection", "server error", "503", "502", "500"]
            )
        if isinstance(error, (ConnectionError, TimeoutError)):
            return True
        return False
    
    async def generate_content(
        self, 
        prompt: str, 
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate content using Gemini 2.5 Flash Lite with retry logic.
        
        Args:
            prompt: The input prompt for generation
            generation_config: Optional configuration parameters
            
        Returns:
            Dictionary containing the generated response and metadata
            
        Raises:
            ValueError: If API key is not configured or input is invalid
            google_exceptions.GoogleAPICallError: If API call fails after retries
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Default generation configuration
        default_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        if generation_config:
            default_config.update(generation_config)
        
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Attempting generation (attempt {attempt + 1}/{self.max_retries + 1})")
                
                # Generate content
                response = self.model.generate_content(
                    prompt,
                    generation_config=default_config
                )
                
                # Validate response
                if not response or not response.text:
                    raise ValueError("Empty response from LLM")
                
                logger.info("Successfully generated content")
                
                return {
                    "success": True,
                    "content": response.text,
                    "prompt_feedback": response.prompt_feedback.dict() if response.prompt_feedback else None,
                    "candidate_count": len(response.candidates) if response.candidates else 0,
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None,
                    "attempt": attempt + 1
                }
                
            except google_exceptions.PermissionDenied as e:
                logger.error(f"Permission denied: {e}")
                raise ValueError("Invalid API key or insufficient permissions") from e
                
            except google_exceptions.NotFound as e:
                logger.error(f"Model not found: {e}")
                raise ValueError("Specified model is not available") from e
                
            except google_exceptions.InvalidArgument as e:
                logger.error(f"Invalid argument: {e}")
                raise ValueError(f"Invalid request parameters: {e}") from e
                
            except google_exceptions.ResourceExhausted as e:
                logger.error(f"Quota exceeded: {e}")
                if attempt < self.max_retries:
                    delay = self._exponential_backoff_delay(attempt)
                    logger.warning(f"Quota exceeded, retrying in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise ValueError("API quota exceeded. Please try again later.") from e
                    
            except (google_exceptions.GoogleAPICallError, ConnectionError, TimeoutError) as e:
                last_error = e
                if attempt < self.max_retries and self._is_retryable_error(e):
                    delay = self._exponential_backoff_delay(attempt)
                    logger.warning(f"Retryable error ({type(e).__name__}), retrying in {delay:.2f} seconds: {e}")
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(f"Non-retryable error or max retries exceeded: {e}")
                    break
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        
        # If we get here, all retries failed
        error_msg = f"Failed to generate content after {self.max_retries + 1} attempts"
        if last_error:
            error_msg += f". Last error: {last_error}"
        
        raise google_exceptions.GoogleAPICallError(error_msg)
    
    async def generate_structured_content(
        self, 
        prompt: str, 
        schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate structured content with JSON output format.
        
        Args:
            prompt: The input prompt
            schema: Optional JSON schema for structured output
            
        Returns:
            Dictionary containing structured response
        """
        # Modify prompt to request JSON output
        json_prompt = f"{prompt}\n\nPlease respond with valid JSON format only."
        if schema:
            json_prompt += f"\n\nFollow this JSON schema: {schema}"
        
        generation_config = {
            "temperature": 0.3,  # Lower temperature for more structured output
            "max_output_tokens": 4096,
        }
        
        try:
            response = await self.generate_content(json_prompt, generation_config)
            
            # Try to parse as JSON if it looks like JSON
            content = response["content"]
            if content.strip().startswith("{") and content.strip().endswith("}"):
                try:
                    import json
                    parsed_content = json.loads(content)
                    response["parsed_content"] = parsed_content
                except json.JSONDecodeError:
                    logger.warning("Failed to parse response as JSON, returning raw text")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate structured content: {e}")
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the LLM service.
        
        Returns:
            Dictionary containing health status information
        """
        try:
            test_prompt = "Respond with 'OK' to confirm the service is working."
            response = await self.generate_content(test_prompt, {"max_output_tokens": 10})
            
            return {
                "status": "healthy",
                "model": "gemini-3.1-flash-lite-preview",
                "api_key_configured": bool(self.api_key),
                "test_response": response["content"][:50] if response.get("content") else None
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "api_key_configured": bool(self.api_key)
            }

# Singleton instance
llm_service = LLMService()
