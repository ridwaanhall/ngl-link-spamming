#!/usr/bin/env python3
"""
NGL Link Spammer - Custom Message Mode

Created by: ridwaanhall
Date: 16/04/2024
Instagram: ridwaanhall

Note: Don't delete this watermark
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ngl_spammer.cli.interface import CLIInterface


def main():
    """Main entry point for custom message mode."""
    cli = CLIInterface(mode="custom")
    cli.run()


if __name__ == "__main__":
    main()
