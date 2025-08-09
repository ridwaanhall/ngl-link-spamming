"""
NGL Link Spammer - A tool for sending messages to NGL.link anonymously.

Created by: ridwaanhall
Date: 16/04/2024
Instagram: ridwaanhall

Note: Don't delete this watermark
"""

__version__ = "2.0.0"
__author__ = "ridwaanhall"
__email__ = "hi@ridwaanhall.com"

from .core.request_sender import RequestSender
from .generators.message_generator import MessageGenerator
from .generators.device_generator import DeviceIDGenerator
from .generators.game_slug_generator import GameSlugGenerator
from .generators.region_generator import UserRegionGenerator

__all__ = [
    "RequestSender",
    "MessageGenerator", 
    "DeviceIDGenerator",
    "GameSlugGenerator",
    "UserRegionGenerator"
]
