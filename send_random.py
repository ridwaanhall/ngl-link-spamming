'''
created by: ridwaanhall
date      : 16/04/2024
instagram : ridwaanhall

note: don't delete this watermark
'''

import os
import sys
import random
import time
import logging
from dotenv import load_dotenv
import requests
from fake_useragent import UserAgent
from generator import MessageGenerator, GameSlugGenerator, DeviceIDGenerator, UserRegionGenerator

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s')

class RequestSender:
    '''
    This class sends requests to the specified URL.
    '''
    def __init__(self, url):
        '''
        Initializes the RequestSender with the specified URL.
        '''
        if not url:
            logging.error("URL must be provided")
            sys.exit(1)
        self.url = url
        self.user_agent = UserAgent()
        self.fake_ip_generator = FakeIPGenerator()

    def send_request(self, username, question, device_id, game_slug, referrer=''):
        '''
        Sends a POST request to the specified URL with the provided parameters.
        '''
        headers = self._generate_headers(username)
        data = {
            'username': username,
            'question': question,
            'deviceId': device_id,
            'gameSlug': game_slug,
            'referrer': referrer
        }
        
        # Add session to maintain cookies and connection pooling
        session = requests.Session()
        
        try:
            response = session.post(self.url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e}")
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Failed: {e}")
            return None
        finally:
            session.close()
        
        return response

    def send_request_with_retry(self, username, question, device_id, game_slug, referrer='', max_retries=3):
        '''
        Sends a POST request to the specified URL with retry the provided parameters.
        '''
        retries = 0
        while retries < max_retries:
            response = self.send_request(username, question, device_id, game_slug, referrer)
            if response is None:
                logging.info("Request failed, retrying...")
                retries += 1
                time.sleep(2)
                continue
            
            if response.status_code == 404:
                logging.error("HTTP Error 404: Not Found. Stopping the program.")
                sys.exit(1)
            
            if response.status_code == 403:
                logging.error("HTTP Error 403: Forbidden. The request was blocked by the server.")
                logging.info("This might be due to rate limiting or IP blocking. Trying different approach...")
                time.sleep(5)  # Wait longer for 403 errors
                retries += 1
                continue
            
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 10))
                logging.info(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retries += 1
                continue

            return response

        logging.error("Max retries reached. Failed to send request.")
        return None

    def _generate_headers(self, username):
        '''
        Generates headers for the request with subtle IP spoofing.
        '''
        fake_ip = self.fake_ip_generator.generate_fake_ip()
        
        # Base headers that are always included
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Dnt': '1',
            'Referer': f'https://ngl.link/{username}',
            'Sec-Ch-Ua': random.choice(['"Microsoft Edge";v="123"', '"Not:A-Brand";v="8"', '"Chromium";v="123"']),
            'Sec-Ch-Ua-Mobile': random.choice(['?0', '?1']),
            'Sec-Ch-Ua-Platform': random.choice(['"Windows"', '"Linux"', '"Macintosh"', '"Android"', '"iOS"']),
            'User-Agent': self.user_agent.random,
        }
        
        # Add fake IP headers randomly and subtly (not all at once)
        ip_headers = [
            'X-Forwarded-For',
            'X-Real-IP', 
            'X-Remote-Addr'
        ]
        
        # Randomly choose 1-2 IP headers to include (more realistic)
        selected_headers = random.sample(ip_headers, random.randint(1, 2))
        for header in selected_headers:
            headers[header] = fake_ip
        
        # Sometimes add additional realistic headers
        if random.random() < 0.3:  # 30% chance
            headers['X-Requested-With'] = 'XMLHttpRequest'
        
        if random.random() < 0.2:  # 20% chance
            headers['Accept-Language'] = random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.8,es;q=0.7',
                'en-US,en;q=0.9,fr;q=0.8'
            ])
        
        return headers

class FakeIPGenerator:
    '''
    This class generates fake IP addresses to avoid rate limiting.
    '''
    
    @staticmethod
    def generate_fake_ip():
        '''
        Generates a random fake IP address.
        '''
        # Generate more realistic IP ranges (common ISP ranges)
        ip_ranges = [
            # Common public IP ranges
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
    def generate_fake_ipv6():
        '''
        Generates a random fake IPv6 address.
        '''
        # Generate 8 groups of 4 hexadecimal digits
        groups = []
        for _ in range(8):
            group = ''.join([random.choice('0123456789abcdef') for _ in range(4)])
            groups.append(group)
        return ':'.join(groups)

if __name__ == "__main__":
    load_dotenv()
    url = "https://ngl.link/api/submit"
    if not url:
        logging.error("No URL provided in environment. Exiting.")
        sys.exit(1)
    pesan = '''
    For better experience, please use a valid username.
    '''
    print(pesan)
    request_sender = RequestSender(url)
    username = input("Enter target username: ").strip().lower()
    if not username:
        logging.error("Username is required. Exiting.")
        sys.exit(1)
    
    spam_choice = input("Do you want to spam? (yes/no): ").lower().strip()
    if spam_choice not in ["yes", "no", "y", "n", ""]:
        logging.error("Invalid choice for spam. Exiting.")
        sys.exit(1)

    device_generator = DeviceIDGenerator()
    message_generator = MessageGenerator()
    game_slug_generator = GameSlugGenerator()
    if spam_choice in ["yes", "y", ""]:
        spam_count = input("How many times do you want to spam? (Default is 9999): ")
        delay_input = input("Enter delay between requests in seconds (Default is 1.0): ").strip()
        try:
            delay = float(delay_input) if delay_input else 1.0
            if delay < 0:
                delay = 1.0
                logging.warning("Negative delay not allowed. Using default 1.0 second.")
        except ValueError:
            delay = 1.0
            logging.warning("Invalid delay format. Using default 1.0 second.")
        
        print()
        spam_count = int(spam_count) if spam_count.isdigit() else 9999

        count_format = f'{{:0{len(str(spam_count))}d}}'

        logging.info(f"Starting spam with {spam_count} messages and {delay} second delay between requests...")
        logging.info("Using subtle IP rotation and realistic headers to avoid detection...")
        print()

        for i in range(spam_count):
            device_id = device_generator.generate_device_id()
            message_input = message_generator.generate_message()
            game_slug = game_slug_generator.generate_game_slug()
            
            response = request_sender.send_request_with_retry(username, message_input, device_id, game_slug)
            if response:
                try:
                    response_data = response.json()
                    question_id = response_data.get("questionId", "Unknown ID")
                    
                    # Get user region code from the response and use the generator to get the full country name
                    user_region_code = response_data.get("userRegion", "Unknown Region")
                    user_region_name = UserRegionGenerator.get_country_name(user_region_code)
                    
                    logging.info(f"({count_format.format(i+1)} of {count_format.format(spam_count)}) {response.status_code} {response.reason} {username.upper()} FROM {user_region_name.upper()} -> '{game_slug.upper()}'") # '{message_input.upper()}'
                except ValueError:
                    logging.error("Failed to decode JSON from response.")
            else:
                logging.error("Failed to send message.")
            
            # Add delay between requests (except for the last one)
            if i < spam_count - 1:
                time.sleep(delay)
    else:
        device_id = device_generator.generate_device_id()
        message_input = message_generator.generate_message()
        game_slug = game_slug_generator.generate_game_slug()
        
        response = request_sender.send_request_with_retry(username, message_input, device_id, game_slug)
        if response:
            try:
                response_data = response.json()
                question_id = response_data.get("questionId", "Unknown ID")
                user_region = response_data.get("userRegion", "Unknown Region")
                logging.info(f"{response.status_code} {response.reason} {user_region} {username.upper()} {game_slug.upper()} -> '{message_input.upper()}'")
            except ValueError:
                logging.error("Failed to decode JSON from response.")
        else:
            logging.error("Failed to send message.")
