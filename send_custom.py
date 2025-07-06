'''
created by: ridwaanhall
date      : 16/04/2024
instagram : ridwaanhall

note: don't delete this watermark
'''

import os
import sys
import random
import string
import time
import logging
from dotenv import load_dotenv
import requests
from fake_useragent import UserAgent

# Configure logging
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

    def send_request(self, username, question, device_id, game_slug='', referrer=''):
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
        try:
            response = requests.post(self.url, headers=headers, data=data)
            response.raise_for_status()  # This will handle HTTP errors which are 400 and above
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Failed: {e}")
            return None
        return response

    def send_request_with_retry(self, username, question, device_id, game_slug='', referrer='', max_retries=3):
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
        Generates headers for the request.
        '''
        return {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Dnt': '1',
            'Referer': f'https://ngl.link/{username}',
            'Sec-Ch-Ua': random.choice(['"Microsoft Edge";v="123"', '"Not:A-Brand";v="8"', '"Chromium";v="123"']),
            'Sec-Ch-Ua-Mobile': random.choice(['?0', '?1']),
            'Sec-Ch-Ua-Platform': random.choice(['"Windows"', '"Linux"', '"Macintosh"', '"Android"', '"iOS"']),
            'User-Agent': self.user_agent.random
        }

class DeviceIDGenerator:
    '''
    Generates device ID for the request.
    '''
    @staticmethod
    def generate_device_id():
        return '-'.join([''.join(random.choices(string.ascii_lowercase + string.digits, k=part_length))
                         for part_length in [8, 4, 4, 4, 12]])

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
    username = input("Enter target username: ").strip()
    if not username:
        logging.error("Username is required. Exiting.")
        sys.exit(1)
    
    spam_choice = input("Do you want to spam? (yes/no): ").lower().strip()
    if spam_choice not in ["yes", "no", "y", "n", ""]:
        logging.error("Invalid choice for spam. Exiting.")
        sys.exit(1)
    
    message_input = input("Enter your message or leave blank to use a default message: ") or " "
    if spam_choice in ["yes", "y", ""]:
        spam_count = input("How many times do you want to spam? (Default is 9999): ")
        spam_count = int(spam_count) if spam_count.isdigit() else 9999
        device_generator = DeviceIDGenerator()

        # Determine the number of digits needed for the spam count
        count_format = f'{{:0{len(str(spam_count))}d}}'

        for i in range(spam_count):
            device_id = device_generator.generate_device_id()
            response = request_sender.send_request_with_retry(username, message_input, device_id)
            if response:
                try:
                    response_data = response.json()
                    question_id = response_data.get("questionId", "Unknown ID")
                    user_region = response_data.get("userRegion", "Unknown Region")
                    logging.info(f"[{count_format.format(i+1)} of {count_format.format(spam_count)}] {response.status_code}:{response.reason} {user_region} {username.upper()} -> '{message_input}'")
                except ValueError:
                    logging.error("Failed to decode JSON from response.")
            else:
                logging.error("Failed to send message.")
    else:
        device_id = os.getenv("DEVICE_ID") or DeviceIDGenerator.generate_device_id()
        response = request_sender.send_request_with_retry(username, message_input, device_id)
        if response:
            try:
                response_data = response.json()
                question_id = response_data.get("questionId", "Unknown ID")
                user_region = response_data.get("userRegion", "Unknown Region")
                logging.info(f'Response: {response.status_code} - {user_region} -> {question_id}')
            except ValueError:
                logging.error("Failed to decode JSON from response.")
        else:
            logging.error("Failed to send message.")
