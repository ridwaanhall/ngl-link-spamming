"""Device ID generator for NGL requests."""

import random
import string
from typing import List


class DeviceIDGenerator:
    """Generates device IDs for NGL requests."""
    
    @staticmethod
    def generate() -> str:
        """Generate a random device ID in UUID-like format.
        
        Returns:
            A device ID string in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        return '-'.join([
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=part_length))
            for part_length in [8, 4, 4, 4, 12]
        ])
    
    @staticmethod
    def generate_batch(count: int) -> List[str]:
        """Generate multiple device IDs.
        
        Args:
            count: Number of device IDs to generate
            
        Returns:
            List of device ID strings
        """
        return [DeviceIDGenerator.generate() for _ in range(count)]
