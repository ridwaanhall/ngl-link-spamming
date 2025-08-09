"""Command-line interface for NGL Link Spammer."""

import sys
from typing import Optional

from ..utils.logger import logger
from ..utils.config import config
from ..core.request_sender import RequestSender
from ..generators.device_generator import DeviceIDGenerator
from ..generators.message_generator import MessageGenerator, MessageType
from ..generators.game_slug_generator import GameSlugGenerator
from ..generators.region_generator import UserRegionGenerator


class CLIInterface:
    """Command-line interface for the NGL Link Spammer."""
    
    def __init__(self, mode: Optional[str] = None):
        """Initialize the CLI interface.
        
        Args:
            mode: Optional mode ('custom', 'random', or None for interactive)
        """
        self.mode = mode
        self.request_sender = RequestSender()
        self.device_generator = DeviceIDGenerator()
        self.message_generator = MessageGenerator()
        self.game_slug_generator = GameSlugGenerator()
    
    def display_welcome_message(self) -> None:
        """Display welcome message and instructions."""
        welcome_message = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           NGL Link Spammer v2.0.0                            ║
║                                                                              ║
║  A professional tool for sending anonymous messages to NGL.link              ║
║                                                                              ║
║  Created by: ridwaanhall                                                     ║
║  Website   : rone.dev                                                        ║
║                                                                              ║
║  For better experience, please use a valid username.                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(welcome_message)
    
    def get_user_input(self) -> dict:
        """Collect user input for the spam operation.
        
        Returns:
            Dictionary containing user preferences
        """
        # Get target username
        username = input("Enter target username: ").strip().lower()
        if not username:
            logger.error("Username is required. Exiting.")
            sys.exit(1)
        
        # Get spam choice
        spam_choice = input("Do you want to spam? (yes/no) [default: yes]: ").lower().strip()
        if spam_choice not in ["yes", "no", "y", "n", ""]:
            logger.error("Invalid choice for spam. Exiting.")
            sys.exit(1)
        
        spam_enabled = spam_choice in ["yes", "y", ""]
        
        # Initialize result dictionary
        result = {
            "username": username,
            "spam_enabled": spam_enabled,
            "spam_count": 1,
            "delay": config.default_delay,
            "custom_message": None
        }
        
        if spam_enabled:
            # Get spam count
            spam_count_input = input(f"How many times do you want to spam? [default: {config.default_spam_count}]: ").strip()
            try:
                result["spam_count"] = int(spam_count_input) if spam_count_input else config.default_spam_count
            except ValueError:
                logger.warning(f"Invalid spam count. Using default: {config.default_spam_count}")
                result["spam_count"] = config.default_spam_count
            
            # Get delay
            delay_input = input(f"Enter delay between requests in seconds [default: {config.default_delay}]: ").strip()
            try:
                delay = float(delay_input) if delay_input else config.default_delay
                if delay < config.min_delay:
                    logger.warning(f"Delay too short. Using minimum: {config.min_delay} seconds")
                    delay = config.min_delay
                result["delay"] = delay
            except ValueError:
                logger.warning(f"Invalid delay format. Using default: {config.default_delay} seconds")
                result["delay"] = config.default_delay
        
        # Ask for custom message based on mode
        if self.mode == "custom":
            custom_message = input("Enter your custom message: ").strip()
            if not custom_message:
                logger.error("Custom message is required in custom mode.")
                sys.exit(1)
            result["custom_message"] = custom_message
        elif self.mode == "random":
            result["custom_message"] = None
            print("📝 Using random generated messages")
        else:
            # Interactive mode - let user choose
            custom_message = input("Enter custom message (leave blank for random): ").strip()
            if custom_message:
                result["custom_message"] = custom_message
        
        return result
    
    def execute_single_request(self, username: str, message: Optional[str] = None) -> None:
        """Execute a single request.
        
        Args:
            username: Target username
            message: Custom message or None for random
        """
        device_id = self.device_generator.generate()
        
        if message:
            question = message
            game_slug = ""
        else:
            question = self.message_generator.generate()
            game_slug = self.game_slug_generator.generate()
        
        response = self.request_sender.send_request_with_retry(username, question, device_id, game_slug)
        
        if response:
            try:
                response_data = response.json()
                question_id = response_data.get("questionId", "Unknown ID")
                user_region_code = response_data.get("userRegion", "Unknown Region")
                user_region_name = UserRegionGenerator.get_country_name(user_region_code)
                
                logger.info(
                    f"✓ {response.status_code} {response.reason} | "
                    f"User: {username.upper()} | "
                    f"Region: {user_region_name.upper()} | "
                    f"Game: {game_slug.upper() if game_slug else 'CUSTOM'} | "
                    f"ID: {question_id}"
                )
            except ValueError:
                logger.error("Failed to decode JSON from response.")
        else:
            logger.error("Failed to send message.")
    
    def execute_spam_requests(
        self, 
        username: str, 
        spam_count: int, 
        delay: float, 
        custom_message: Optional[str] = None
    ) -> None:
        """Execute multiple spam requests.
        
        Args:
            username: Target username
            spam_count: Number of requests to send
            delay: Delay between requests
            custom_message: Custom message or None for random
        """
        logger.info(f"Starting spam operation:")
        logger.info(f"  • Target: {username}")
        logger.info(f"  • Messages: {spam_count}")
        logger.info(f"  • Base delay: {delay}s")
        logger.info(f"  • Message type: {'Custom' if custom_message else 'Random'}")
        logger.info("  • Using adaptive timing and IP rotation to avoid detection...")
        print()
        
        # Format string for progress counter
        count_format = f'{{:0{len(str(spam_count))}d}}'
        
        success_count = 0
        error_count = 0
        
        # Set initial delay for the delay manager
        self.request_sender.delay_manager.current_delay = delay
        
        for i in range(spam_count):
            device_id = self.device_generator.generate()
            
            if custom_message:
                question = custom_message
                game_slug = ""
            else:
                question = self.message_generator.generate()
                game_slug = self.game_slug_generator.generate()
            
            response = self.request_sender.send_request_with_retry(username, question, device_id, game_slug)
            
            if response:
                try:
                    response_data = response.json()
                    question_id = response_data.get("questionId", "Unknown ID")
                    user_region_code = response_data.get("userRegion", "Unknown Region")
                    user_region_name = UserRegionGenerator.get_country_name(user_region_code)
                    
                    if response.status_code == 200:
                        success_count += 1
                        status_icon = "✓"
                    else:
                        error_count += 1
                        status_icon = "✗"
                    
                    progress = f"({count_format.format(i+1)}/{count_format.format(spam_count)})"
                    message_type = game_slug.upper() if game_slug else 'CUSTOM'
                    
                    logger.info(
                        f"{status_icon} {progress} {response.status_code} {response.reason} | "
                        f"{username.upper()} FROM {user_region_name.upper()} → {message_type}"
                    )
                    
                except ValueError:
                    error_count += 1
                    logger.error(f"✗ ({count_format.format(i+1)}/{count_format.format(spam_count)}) Failed to decode JSON from response.")
            else:
                error_count += 1
                logger.error(f"✗ ({count_format.format(i+1)}/{count_format.format(spam_count)}) Failed to send message.")
            
            # Adaptive delay adjustment every 5 requests
            if (i + 1) % 5 == 0:
                old_delay = self.request_sender.delay_manager.current_delay
                new_delay = self.request_sender.delay_manager.calculate_delay()
                
                if new_delay != old_delay:
                    logger.info(f"🔄 Adjusted delay to {new_delay:.1f}s (Success: {success_count}, Errors: {error_count})")
                
                # Reset counters periodically
                if error_count > 0:
                    self.request_sender.delay_manager.reset_counters()
            
            # Add delay between requests (except for the last one)
            if i < spam_count - 1:
                self.request_sender.delay_manager.wait_with_jitter()
        
        # Display final statistics
        print()
        logger.info("📊 Final Statistics:")
        logger.info(f"  • Total requests: {spam_count}")
        logger.info(f"  • Successful: {success_count}")
        logger.info(f"  • Failed: {error_count}")
        logger.info(f"  • Success rate: {(success_count/spam_count)*100:.1f}%")
    
    def run(self) -> None:
        """Run the CLI interface."""
        try:
            self.display_welcome_message()
            user_input = self.get_user_input()
            
            if user_input["spam_enabled"]:
                self.execute_spam_requests(
                    username=user_input["username"],
                    spam_count=user_input["spam_count"],
                    delay=user_input["delay"],
                    custom_message=user_input["custom_message"]
                )
            else:
                self.execute_single_request(
                    username=user_input["username"],
                    message=user_input["custom_message"]
                )
                
        except KeyboardInterrupt:
            logger.info("\n⚠️  Operation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)
        finally:
            # Clean up resources
            self.request_sender.close_session()
