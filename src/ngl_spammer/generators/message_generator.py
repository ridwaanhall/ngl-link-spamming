"""Message generator for NGL requests."""

import random
from typing import List, Optional
from enum import Enum


class MessageType(Enum):
    """Types of messages that can be generated."""
    GENERIC = "generic"
    HACKER = "hacker"
    RANDOM = "random"


class MessageGenerator:
    """Generates various types of messages for NGL requests."""
    
    def __init__(self):
        """Initialize the message generator with predefined messages."""
        self.generic_messages = [
            "Hey there! Just wanted to drop a quick message to say hi and see how you're doing. Hope you're having a great day! 😊",
            "Hi friend! Sending some positive vibes your way. Hope you're doing well!",
            "Hey buddy! Remember, you're awesome and capable of achieving anything you set your mind to! 💪",
            "Hello! Just checking in to see how you're doing. Let me know if there's anything I can do to support you!",
            "Hi! Wishing you a fantastic day filled with joy and laughter. Keep shining bright! ✨",
            "Hey! Hope your day is as amazing as you are! 😄",
            "Hi there! Just wanted to remind you that you're appreciated and valued. Keep being awesome!",
            "Hey friend! Just dropping by to say hello and spread some positivity your way. Have a wonderful day!",
            "Hello! Sending you lots of love and good vibes. You've got this!",
            "Hi! Remember, every challenge you face is an opportunity to grow stronger. Keep pushing forward!",
            "Hey there! Just wanted to send a quick virtual hug your way. You're not alone, and I'm here for you!",
            "Hi friend! Hope your day is filled with laughter, love, and all the good things in life. You deserve it!"
        ]
        
        self.hacker_messages = [
            "Initiating secure connection. Your digital presence is attracting attention. Stay vigilant. - ShadowCipher",
            "Warning: Unusual activity detected in your online behavior. Exercise caution. - DarkNetOp",
            "Cipher protocol activated. Your online actions have drawn scrutiny. Maintain discretion. - GhostHacker",
            "Alert: Anomaly detected in network traffic. You may be under surveillance. - StealthByte",
            "Security breach alert: Your digital footprint is being monitored. Take evasive action. - PhantomByte",
            "Caution: Digital surveillance detected. Your activities are being watched closely. - CyberPhantom",
            "Intrusion warning: Your online presence is under scrutiny. Stay under the radar. - CryptoGhost",
            "Encryption compromised. Your digital identity may be at risk. Take precautions. - ShadowCipher",
            "Attention: Suspicious network activity detected. Exercise heightened security measures. - DarkNetOp",
            "Security protocol breached. Your digital security may have been compromised. - GhostHacker",
            "Warning: Abnormal data flow detected in your network. Stay alert. - StealthByte",
            "Code red: Unauthorized access detected. Your online security is under threat. - PhantomByte",
            "Initiating secure transmission. Your digital activities have attracted attention. Stay covert. - CyberPhantom",
            "Caution: Anomalies detected in network traffic. Proceed with caution. - CryptoGhost",
            "Alert: Cipher protocol engaged. Your online presence may be compromised. - ShadowCipher",
            "Security breach detected. Your digital identity is vulnerable. Take action. - DarkNetOp",
            "Warning: Digital surveillance in progress. Maintain operational security. - GhostHacker",
            "Attention: Unusual patterns detected in your online behavior. Stay under the radar. - StealthByte",
            "Intrusion alert: Your online activities are being monitored. Stay low-key. - PhantomByte",
            "Encryption compromised. Your digital security may be compromised. Take evasive action. - CyberPhantom",
            "Alert: Suspicious network activity detected. Exercise caution in your online interactions. - CryptoGhost",
            "Security protocol breached. Your digital footprint is attracting unwanted attention. - ShadowCipher",
            "Code red: Unauthorized access detected. Take measures to protect your online security. - DarkNetOp",
            "Initiating secure communication. Your digital presence is under scrutiny. Maintain discretion. - GhostHacker",
            "Caution: Abnormal data flow detected. Your online activities may be compromised. - StealthByte",
            "Alert: Cipher protocol activated. Your digital security is at risk. Take precautions. - PhantomByte",
            "Security breach detected. Your digital privacy may be compromised. Take evasive action. - CyberPhantom",
            "Warning: Digital surveillance detected. Exercise caution in your online interactions. - CryptoGhost",
            "Attention: Unusual activity detected in your network. Stay alert. - ShadowCipher",
            "Intrusion warning: Your digital footprint has been noticed. Stay under the radar. - DarkNetOp"
        ]
    
    def generate(self, message_type: MessageType = MessageType.RANDOM) -> str:
        """Generate a message of the specified type.
        
        Args:
            message_type: Type of message to generate
            
        Returns:
            Generated message string
        """
        if message_type == MessageType.GENERIC:
            return random.choice(self.generic_messages)
        elif message_type == MessageType.HACKER:
            return random.choice(self.hacker_messages)
        else:  # RANDOM
            # Heavily favor hacker messages (like original code)
            if random.random() < 1.0:  # Always hacker messages for now
                return random.choice(self.hacker_messages)
            else:
                return random.choice(self.generic_messages)
    
    def add_custom_messages(self, messages: List[str], message_type: MessageType = MessageType.GENERIC) -> None:
        """Add custom messages to the generator.
        
        Args:
            messages: List of custom messages to add
            message_type: Type of messages being added
        """
        if message_type == MessageType.GENERIC:
            self.generic_messages.extend(messages)
        elif message_type == MessageType.HACKER:
            self.hacker_messages.extend(messages)
    
    def get_message_count(self, message_type: Optional[MessageType] = None) -> int:
        """Get the count of available messages.
        
        Args:
            message_type: Specific type to count, or None for total
            
        Returns:
            Number of available messages
        """
        if message_type == MessageType.GENERIC:
            return len(self.generic_messages)
        elif message_type == MessageType.HACKER:
            return len(self.hacker_messages)
        else:
            return len(self.generic_messages) + len(self.hacker_messages)
