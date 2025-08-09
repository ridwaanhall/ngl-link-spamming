"""Network utilities for request handling."""

import random
import time
from typing import Optional, Dict, Any

from .config import config
from .logger import logger


class AdaptiveDelayManager:
    """Manages adaptive delays between requests to avoid rate limiting."""
    
    def __init__(self, initial_delay: float = None):
        """Initialize with optional custom delay."""
        self.current_delay = initial_delay or config.default_delay
        self.success_count = 0
        self.error_count = 0
    
    def calculate_delay(self) -> float:
        """Calculate adaptive delay based on success/error ratio."""
        if self.error_count > 0:
            # More aggressive increase when hitting rate limits
            self.current_delay = min(self.current_delay * 2.0, config.max_delay)
        elif self.success_count > self.error_count * 5 and self.current_delay > config.min_delay:
            # Only decrease delay if we have a very good success rate
            self.current_delay = max(self.current_delay * 0.9, config.min_delay)
        
        return self.current_delay
    
    def record_success(self) -> None:
        """Record a successful request."""
        self.success_count += 1
    
    def record_error(self) -> None:
        """Record a failed request."""
        self.error_count += 1
    
    def reset_counters(self) -> None:
        """Reset success and error counters."""
        self.success_count = 0
        self.error_count = 0
    
    def wait_with_jitter(self) -> None:
        """Wait with calculated delay plus random jitter."""
        delay = self.calculate_delay()
        # Add random variation to avoid patterns
        jittered_delay = delay + random.uniform(-0.5, 1.0)
        if jittered_delay < config.min_delay:
            jittered_delay = config.min_delay
        
        logger.debug(f"Waiting {jittered_delay:.2f} seconds")
        time.sleep(jittered_delay)


class RateLimitHandler:
    """Handles rate limiting responses from the server."""
    
    @staticmethod
    def handle_rate_limit(response_headers: Dict[str, Any]) -> float:
        """Handle rate limit response and return wait time.
        
        Args:
            response_headers: Response headers from rate limited request
            
        Returns:
            Time to wait in seconds
        """
        retry_after = int(response_headers.get('Retry-After', config.rate_limit_wait_base))
        # Add substantial randomness for 429 errors
        wait_time = retry_after + random.uniform(
            config.rate_limit_wait_random_min,
            config.rate_limit_wait_random_max
        )
        
        logger.warning(f"Rate limited. Retrying after {wait_time:.1f} seconds...")
        return wait_time


class IPGenerator:
    """Generates fake IP addresses for header spoofing."""
    
    @staticmethod
    def generate_ipv4() -> str:
        """Generate a realistic fake IPv4 address."""
        # Generate more realistic IP ranges (common ISP ranges)
        ip_ranges = [
            (1, 126),    # Class A
            (128, 191),  # Class B  
            (192, 223),  # Class C
        ]
        
        # Choose a random range
        start, end = random.choice(ip_ranges)
        first_octet = random.randint(start, end)
        
        # Avoid obviously fake patterns
        remaining_octets = [
            random.randint(1, 254),
            random.randint(1, 254), 
            random.randint(1, 254)
        ]
        
        return f"{first_octet}.{'.'.join(map(str, remaining_octets))}"
    
    @staticmethod
    def generate_ipv6() -> str:
        """Generate a fake IPv6 address."""
        # Generate 8 groups of 4 hexadecimal digits
        groups = []
        for _ in range(8):
            group = ''.join([random.choice('0123456789abcdef') for _ in range(4)])
            groups.append(group)
        return ':'.join(groups)
