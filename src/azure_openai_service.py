"""Azure OpenAI service module with proper error handling and security."""
import os
import logging
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables - ensure we load from the correct path
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """Service class for Azure OpenAI integration with error handling and retry logic."""
    
    def __init__(self):
        """Initialize Azure OpenAI client with configuration from environment variables."""
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
        # Load custom system message from environment variable
        self.system_message = os.getenv("AZURE_OPENAI_SYSTEM_MESSAGE", 
                                       "You are a helpful AI assistant. Provide clear, concise, and helpful responses related to Kubernetes only.")
        
        # Debug logging
        logger.info(f"Loading Azure OpenAI configuration:")
        logger.info(f"Endpoint: {self.endpoint}")
        logger.info(f"API Key: {'***' + self.api_key[-4:] if self.api_key else 'None'}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Deployment: {self.deployment_name}")
        logger.info(f"System Message: {self.system_message[:50]}{'...' if len(self.system_message) > 50 else ''}")
        
        # Validate required configuration
        if not self.endpoint or not self.api_key:
            logger.error("Missing required Azure OpenAI configuration in environment variables")
            raise ValueError("Missing required Azure OpenAI configuration in environment variables")
        
        # Initialize headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        # Check if endpoint already contains the full URL or just the base
        if "chat/completions" in self.endpoint:
            # Full URL provided in endpoint
            self.api_url = self.endpoint
        else:
            # Base endpoint provided, build the full URL
            self.api_url = f"{self.endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        logger.info(f"Using API URL: {self.api_url}")
        logger.info("Azure OpenAI service initialized successfully")
    
    def generate_response(self, user_message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response from Azure OpenAI.
        
        Args:
            user_message (str): The user's input message
            conversation_history (list, optional): Previous conversation context
            
        Returns:
            str: Generated response from Azure OpenAI
        """
        try:
            # Prepare messages for the API
            messages = []
            
            # Add system message for context (now configurable)
            messages.append({
                "role": "system",
                "content": self.system_message
            })
            
            # Add conversation history if provided
            if conversation_history:
                # Take last 10 messages to avoid token limit issues
                recent_history = conversation_history[-10:]
                for msg in recent_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare the request payload - using only supported parameters for gpt-5-mini
            payload = {
                "messages": messages,
                "max_completion_tokens": 800
            }
            
            # Make API call with proper error handling
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    generated_response = response_data["choices"][0]["message"]["content"].strip()
                    logger.info("Successfully generated response from Azure OpenAI")
                    return generated_response
                else:
                    logger.warning("No response generated from Azure OpenAI")
                    return "I apologize, but I couldn't generate a response at the moment. Please try again."
            else:
                logger.error(f"Azure OpenAI API error: {response.status_code} - {response.text}")
                return "I'm sorry, I'm experiencing some technical difficulties. Please try again in a moment."
                
        except Exception as e:
            logger.error(f"Error generating response from Azure OpenAI: {e}")
            # Return a user-friendly error message instead of exposing technical details
            return "I'm sorry, I'm experiencing some technical difficulties. Please try again in a moment."
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return bool(self.endpoint and self.api_key and self.api_url)

class ChatService:
    """Service class for managing both Azure OpenAI and Local Chat API."""

    def __init__(self):
        """Initialize the service based on environment variables."""
        self.use_local_api = os.getenv("USE_LOCAL_API", "false").lower() == "true"

        if self.use_local_api:
            self.base_url = os.getenv("LOCAL_CHAT_API_BASE_URL")
            self.endpoint = os.getenv("LOCAL_CHAT_API_ENDPOINT")
            self.api_url = f"{self.base_url.rstrip('/')}{self.endpoint}"
            logger.info(f"Using Local Chat API: {self.api_url}")
        else:
            self.azure_service = AzureOpenAIService()

    def generate_response(self, user_message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response using the selected API.

        Args:
            user_message (str): The user's input message
            conversation_history (list, optional): Previous conversation context

        Returns:
            str: Generated response
        """
        if self.use_local_api:
            try:
                # Format messages for the local API
                messages = []
                # Add conversation history if provided
                if conversation_history:
                    messages.extend([{
                        "role": msg["role"],
                        "content": msg["content"]
                    } for msg in conversation_history])
                
                # Add current user message
                messages.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Prepare payload for local API
                payload = {
                    "messages": messages
                }
                
                logger.info(f"Sending request to local API with payload: {json.dumps(payload)}")
                response = requests.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    logger.info(f"Received response from local API: {json.dumps(response_data)}")
                    return response_data.get("response", "No response from local API.")
                else:
                    logger.error(f"Local API error: {response.status_code} - {response.text}")
                    return f"Error communicating with the local API: {response.text}"
            except Exception as e:
                logger.error(f"Error using Local Chat API: {e}")
                return "Technical difficulties with the local API."
        else:
            return self.azure_service.generate_response(user_message, conversation_history)

    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        if self.use_local_api:
            return bool(self.base_url and self.endpoint)
        return self.azure_service.is_configured()

# Global instance for use across the application
chat_service = ChatService()