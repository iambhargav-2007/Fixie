"""Application settings and environment configuration."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Settings
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"

    # Database Settings
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "fixfind"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"), 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    def get_llm(self):
        """Returns the centralized LLM instance for all agents."""
        # This is a basic abstraction for the LLM. 
        # For now, it simply demonstrates how an LLM would be initialized.
        # It's kept simple without tightly coupling to one specific provider's full implementation yet.
        
        # Example pseudo-code for initialization (will be expanded later):
        # from langchain_openai import ChatOpenAI
        # return ChatOpenAI(model=self.LLM_MODEL, api_key=self.LLM_API_KEY)
        
        # return f"MockLLM({self.LLM_MODEL})"
        try:
            from langchain_openai import ChatOpenAI
            
            # Default to a robust multimodal model on OpenRouter if not specified
            model = self.LLM_MODEL if self.LLM_MODEL and self.LLM_MODEL != "GROQ" else "openai/gpt-4o-mini"
            
            # If the user is using OpenRouter (starts with sk-or)
            if self.LLM_API_KEY.startswith("sk-or"):
                return ChatOpenAI(
                    model=model, 
                    api_key=self.LLM_API_KEY, 
                    base_url="https://openrouter.ai/api/v1"
                )
            # Fallback to OpenAI directly
            return ChatOpenAI(model=model, api_key=self.LLM_API_KEY)
        except ImportError:
            import logging
            logging.warning("langchain_openai not installed. Returning MockLLM.")
            return f"MockLLM({self.LLM_MODEL})"


# Singleton settings instance
settings = Settings()
