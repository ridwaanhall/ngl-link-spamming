#!/usr/bin/env python3
"""
NGL Link Spammer - Random Message Mode

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
    """Main entry point for random message mode."""
    cli = CLIInterface(mode="random")
    cli.run()


if __name__ == "__main__":
    main()
