"""Tests for message generator."""

import pytest
from ngl_spammer.generators.message_generator import MessageGenerator, MessageType


class TestMessageGenerator:
    """Test cases for MessageGenerator."""
    
    def test_init(self):
        """Test MessageGenerator initialization."""
        generator = MessageGenerator()
        assert len(generator.generic_messages) > 0
        assert len(generator.hacker_messages) > 0
    
    def test_generate_generic_message(self):
        """Test generating generic messages."""
        generator = MessageGenerator()
        message = generator.generate(MessageType.GENERIC)
        
        assert message in generator.generic_messages
        assert len(message) > 0
    
    def test_generate_hacker_message(self):
        """Test generating hacker messages."""
        generator = MessageGenerator()
        message = generator.generate(MessageType.HACKER)
        
        assert message in generator.hacker_messages
        assert len(message) > 0
    
    def test_generate_random_message(self):
        """Test generating random messages."""
        generator = MessageGenerator()
        message = generator.generate(MessageType.RANDOM)
        
        # Should be from either category
        assert (message in generator.generic_messages or 
                message in generator.hacker_messages)
    
    def test_add_custom_messages(self):
        """Test adding custom messages."""
        generator = MessageGenerator()
        custom_messages = ["Custom message 1", "Custom message 2"]
        
        initial_count = len(generator.generic_messages)
        generator.add_custom_messages(custom_messages, MessageType.GENERIC)
        
        assert len(generator.generic_messages) == initial_count + 2
        for msg in custom_messages:
            assert msg in generator.generic_messages
    
    def test_get_message_count(self):
        """Test message count functionality."""
        generator = MessageGenerator()
        
        generic_count = generator.get_message_count(MessageType.GENERIC)
        hacker_count = generator.get_message_count(MessageType.HACKER)
        total_count = generator.get_message_count()
        
        assert generic_count == len(generator.generic_messages)
        assert hacker_count == len(generator.hacker_messages)
        assert total_count == generic_count + hacker_count
