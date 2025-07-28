"""Claude API wrapper for article generation"""
import os
import json
import time
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class ClaudeAPI:
    """Wrapper for Claude API with retry logic and error handling"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate completion with retry logic"""
        try:
            start_time = time.time()
            
            messages = [{"role": "user", "content": prompt}]
            
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                system=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            elapsed_time = time.time() - start_time
            
            # Log metadata
            if metadata:
                logger.info(f"API call completed in {elapsed_time:.2f}s", extra={
                    "phase": metadata.get("phase"),
                    "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
                })
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise
    
    def generate_with_structured_output(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        expected_format: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion and parse as JSON"""
        
        # Add format instructions to prompt if provided
        if expected_format:
            format_instruction = f"\n\nPlease provide your response in the following JSON format:\n{json.dumps(expected_format, indent=2)}\n\nIMPORTANT: Return ONLY valid JSON without any additional text or markdown formatting."
            prompt = prompt + format_instruction
        
        # Add JSON-specific system prompt enhancement
        enhanced_system = system_prompt or ""
        enhanced_system += "\n\nAlways respond with valid JSON format only. Do not include any explanatory text outside the JSON structure."
        
        response = self.generate_completion(
            prompt=prompt,
            system_prompt=enhanced_system,
            **kwargs
        )
        
        # Try to extract JSON from response
        try:
            # Clean up common formatting issues
            cleaned_response = response.strip()
            
            # Look for JSON block in response
            if "```json" in cleaned_response:
                json_start = cleaned_response.find("```json") + 7
                json_end = cleaned_response.find("```", json_start)
                json_str = cleaned_response[json_start:json_end].strip()
            elif "```" in cleaned_response:
                # Handle case where it's just wrapped in ``` without json label
                json_start = cleaned_response.find("```") + 3
                json_end = cleaned_response.find("```", json_start)
                json_str = cleaned_response[json_start:json_end].strip()
            else:
                # Assume entire response is JSON
                json_str = cleaned_response
            
            # Remove any potential BOM or zero-width spaces
            json_str = json_str.lstrip('\ufeff').strip()
            
            # Parse the JSON
            parsed_data = json.loads(json_str)
            
            # Validate that we got a dictionary (not a list or primitive)
            if not isinstance(parsed_data, dict):
                raise ValueError(f"Expected JSON object, got {type(parsed_data).__name__}")
            
            return parsed_data
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response length: {len(response)}")
            logger.error(f"Response preview: {repr(response[:200])}")
            if 'json_str' in locals():
                logger.error(f"JSON string preview: {repr(json_str[:200])}")
            
            # Also log character codes to debug invisible characters
            if len(response) > 0:
                first_chars = [ord(c) for c in response[:10]]
                logger.error(f"First 10 character codes: {first_chars}")
            
            # Return raw response as fallback
            return {"raw_response": response, "parse_error": str(e)}
    
    def batch_generate(
        self,
        prompts: List[Dict[str, Any]],
        max_concurrent: int = 5
    ) -> List[str]:
        """Generate multiple completions in batch"""
        results = []
        
        # Simple sequential processing for now
        # TODO: Implement proper async batch processing
        for prompt_data in prompts:
            result = self.generate_completion(**prompt_data)
            results.append(result)
        
        return results