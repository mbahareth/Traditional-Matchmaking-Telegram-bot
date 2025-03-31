#!/usr/bin/env python3
"""
Entry point script for the Traditional Matchmaking Telegram Bot.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.bot import main

if __name__ == "__main__":
    main()
