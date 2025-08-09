"""Game slug generator for NGL requests."""

import random
from typing import List


class GameSlugGenerator:
    """Generates game slugs for NGL requests."""
    
    def __init__(self):
        """Initialize with predefined game slugs."""
        self.game_slugs = [
            "",  # Empty slug
            "confessions",  
            "3words",  
            "tbh",  
            "shipme",  
            "yourcrush",  
            "cancelled",  
            "dealbreaker"  
        ]
    
    def generate(self) -> str:
        """Generate a random game slug.
        
        Returns:
            Random game slug string
        """
        return random.choice(self.game_slugs)
    
    def add_custom_slugs(self, slugs: List[str]) -> None:
        """Add custom game slugs.
        
        Args:
            slugs: List of custom game slugs to add
        """
        self.game_slugs.extend(slugs)
    
    def get_available_slugs(self) -> List[str]:
        """Get list of all available game slugs.
        
        Returns:
            List of available game slug strings
        """
        return self.game_slugs.copy()
    
    def get_slug_count(self) -> int:
        """Get the count of available game slugs.
        
        Returns:
            Number of available game slugs
        """
        return len(self.game_slugs)
