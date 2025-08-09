"""Configuration management for NGL Link Spammer."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # API Configuration
    ngl_api_url: str = "https://ngl.link/api/submit"
    
    # Request Configuration
    default_timeout: int = 10
    max_retries: int = 3
    default_delay: float = 3.0
    min_delay: float = 1.0
    max_delay: float = 15.0
    
    # Spam Configuration
    default_spam_count: int = 9999
    
    # Rate Limiting
    rate_limit_wait_base: int = 20
    rate_limit_wait_random_min: float = 5.0
    rate_limit_wait_random_max: float = 15.0
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "[%(asctime)s - %(levelname)s] %(message)s"
    
    # Headers Configuration
    ip_header_probability: float = 0.6
    xhr_header_probability: float = 0.4
    lang_header_probability: float = 0.3
    encoding_header_probability: float = 0.2
    connection_header_probability: float = 0.3
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        load_dotenv()
        
        return cls(
            ngl_api_url=os.getenv("NGL_API_URL", cls.ngl_api_url),
            default_timeout=int(os.getenv("DEFAULT_TIMEOUT", cls.default_timeout)),
            max_retries=int(os.getenv("MAX_RETRIES", cls.max_retries)),
            default_delay=float(os.getenv("DEFAULT_DELAY", cls.default_delay)),
            min_delay=float(os.getenv("MIN_DELAY", cls.min_delay)),
            max_delay=float(os.getenv("MAX_DELAY", cls.max_delay)),
            default_spam_count=int(os.getenv("DEFAULT_SPAM_COUNT", cls.default_spam_count)),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
        )


# Global configuration instance
config = AppConfig.load_from_env()
