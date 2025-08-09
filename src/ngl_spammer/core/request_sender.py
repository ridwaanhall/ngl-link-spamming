"""Core request sender for NGL Link Spammer."""

import sys
import random
import time
from typing import Optional, Dict, Any, List
import requests
from fake_useragent import UserAgent

from ..utils.config import config
from ..utils.logger import logger
from ..utils.network import AdaptiveDelayManager, RateLimitHandler, IPGenerator


class RequestSender:
    """Handles sending requests to NGL.link API with advanced features."""
    
    def __init__(self, url: Optional[str] = None):
        """Initialize the RequestSender.
        
        Args:
            url: API URL to send requests to. Uses config default if not provided.
        """
        self.url = url or config.ngl_api_url
        if not self.url:
            logger.error("URL must be provided")
            sys.exit(1)
            
        self.user_agent = UserAgent()
        self.ip_generator = IPGenerator()
        self.session = requests.Session()  # Reuse session for connection pooling
        self.delay_manager = AdaptiveDelayManager()
        self.rate_limit_handler = RateLimitHandler()
    
    def send_request(
        self, 
        username: str, 
        question: str, 
        device_id: str, 
        game_slug: str = '', 
        referrer: str = ''
    ) -> Optional[requests.Response]:
        """Send a single POST request to the NGL API.
        
        Args:
            username: Target username
            question: Message/question to send
            device_id: Device ID for the request
            game_slug: Game slug (optional)
            referrer: Referrer URL (optional)
            
        Returns:
            Response object or None if request failed
        """
        headers = self._generate_headers(username)
        data = {
            'username': username,
            'question': question,
            'deviceId': device_id,
            'gameSlug': game_slug,
            'referrer': referrer
        }
        
        response = None
        try:
            response = self.session.post(
                self.url, 
                headers=headers, 
                data=data, 
                timeout=config.default_timeout
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            return response  # Return response even with HTTP error for status code checking
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Failed: {e}")
            return None
    
    def send_request_with_retry(
        self, 
        username: str, 
        question: str, 
        device_id: str, 
        game_slug: str = '', 
        referrer: str = '', 
        max_retries: Optional[int] = None
    ) -> Optional[requests.Response]:
        """Send a POST request with retry logic and rate limiting handling.
        
        Args:
            username: Target username
            question: Message/question to send
            device_id: Device ID for the request
            game_slug: Game slug (optional)
            referrer: Referrer URL (optional)
            max_retries: Maximum number of retries (uses config default if not provided)
            
        Returns:
            Response object or None if all retries failed
        """
        max_retries = max_retries or config.max_retries
        retries = 0
        
        while retries < max_retries:
            response = self.send_request(username, question, device_id, game_slug, referrer)
            
            if response is None:
                logger.info("Request failed, retrying...")
                self.delay_manager.record_error()
                retries += 1
                time.sleep(2)
                continue
            
            # Handle specific HTTP status codes
            if response.status_code == 404:
                logger.error("HTTP Error 404: Not Found. User may not exist.")
                sys.exit(1)
            
            if response.status_code == 403:
                logger.error("HTTP Error 403: Forbidden. The request was blocked by the server.")
                logger.info("This might be due to rate limiting or IP blocking. Trying different approach...")
                self.delay_manager.record_error()
                time.sleep(5)  # Wait longer for 403 errors
                retries += 1
                continue
            
            if response.status_code == 429:
                wait_time = self.rate_limit_handler.handle_rate_limit(response.headers)
                time.sleep(wait_time)
                retries += 1
                continue
            
            # Success case
            if response.status_code == 200:
                self.delay_manager.record_success()
            else:
                self.delay_manager.record_error()
                
            return response
        
        logger.error("Max retries reached. Failed to send request.")
        return None
    
    def send_bulk_requests(
        self,
        username: str,
        requests_data: List[Dict[str, Any]],
        delay_between_requests: Optional[float] = None
    ) -> List[Optional[requests.Response]]:
        """Send multiple requests with adaptive delays.
        
        Args:
            username: Target username
            requests_data: List of dictionaries containing request data
            delay_between_requests: Fixed delay between requests (optional)
            
        Returns:
            List of response objects (or None for failed requests)
        """
        responses = []
        
        for i, request_data in enumerate(requests_data):
            response = self.send_request_with_retry(
                username=username,
                question=request_data.get('question', ''),
                device_id=request_data.get('device_id', ''),
                game_slug=request_data.get('game_slug', ''),
                referrer=request_data.get('referrer', '')
            )
            
            responses.append(response)
            
            # Add delay between requests (except for the last one)
            if i < len(requests_data) - 1:
                if delay_between_requests:
                    time.sleep(delay_between_requests)
                else:
                    self.delay_manager.wait_with_jitter()
        
        return responses
    
    def _generate_headers(self, username: str) -> Dict[str, str]:
        """Generate headers for the request with realistic variations.
        
        Args:
            username: Target username for referer header
            
        Returns:
            Dictionary of HTTP headers
        """
        fake_ip = self.ip_generator.generate_ipv4()
        
        # Base headers that are always included
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Dnt': '1',
            'Referer': f'https://ngl.link/{username}',
            'Sec-Ch-Ua': random.choice([
                '"Microsoft Edge";v="123"', 
                '"Not:A-Brand";v="8"', 
                '"Chromium";v="123"'
            ]),
            'Sec-Ch-Ua-Mobile': random.choice(['?0', '?1']),
            'Sec-Ch-Ua-Platform': random.choice([
                '"Windows"', '"Linux"', '"Macintosh"', '"Android"', '"iOS"'
            ]),
            'User-Agent': self.user_agent.random,
        }
        
        # Add fake IP headers randomly and subtly (not all at once)
        if random.random() < config.ip_header_probability:
            ip_headers = ['X-Forwarded-For', 'X-Real-IP', 'X-Remote-Addr']
            selected_headers = random.sample(ip_headers, random.randint(1, 2))
            for header in selected_headers:
                headers[header] = fake_ip
        
        # Sometimes add additional realistic headers
        if random.random() < config.xhr_header_probability:
            headers['X-Requested-With'] = 'XMLHttpRequest'
        
        if random.random() < config.lang_header_probability:
            headers['Accept-Language'] = random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.8,es;q=0.7',
                'en-US,en;q=0.9,fr;q=0.8',
                'id-ID,id;q=0.9,en;q=0.8'
            ])
        
        if random.random() < config.encoding_header_probability:
            headers['Accept-Encoding'] = random.choice([
                'gzip, deflate, br',
                'gzip, deflate',
                'gzip'
            ])
        
        # Add random connection header
        if random.random() < config.connection_header_probability:
            headers['Connection'] = random.choice(['keep-alive', 'close'])
        
        return headers
    
    def get_delay_manager(self) -> AdaptiveDelayManager:
        """Get the current delay manager instance.
        
        Returns:
            AdaptiveDelayManager instance
        """
        return self.delay_manager
    
    def reset_delay_manager(self) -> None:
        """Reset the delay manager to initial state."""
        self.delay_manager = AdaptiveDelayManager()
    
    def close_session(self) -> None:
        """Close the requests session."""
        self.session.close()
