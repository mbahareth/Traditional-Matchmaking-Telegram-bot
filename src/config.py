"""
Configuration settings for the Traditional Matchmaking Telegram Bot.
"""

import os
from pathlib import Path

# Bot Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7606109523:AAF_b16juzJh0jGCCt7fQ7zwy7DFn6ekpxQ")  # Token provided by user

# Database Configuration
DB_PATH = Path(__file__).parent.parent / "data" / "matchmaking.db"
DB_URI = f"sqlite:///{DB_PATH}"

# Feature Flags
ENABLE_PERSONALITY_TEST = True
ENABLE_HOROSCOPE = True
ENABLE_ARABIC_TRANSLATION = True
ENABLE_FAMILY_INVOLVEMENT = True

# Matching Algorithm Weights
RELIGIOUS_COMPATIBILITY_WEIGHT = 0.30
PERSONALITY_COMPATIBILITY_WEIGHT = 0.25
FAMILY_VALUES_WEIGHT = 0.20
LIFESTYLE_COMPATIBILITY_WEIGHT = 0.15
HOROSCOPE_COMPATIBILITY_WEIGHT = 0.10

# User Interface Settings
DEFAULT_LANGUAGE = "en"  # 'en' for English, 'ar' for Arabic
MAX_DAILY_MATCHES = 5
MAX_ACTIVE_CONVERSATIONS = 10

# Security Settings
PROFILE_PHOTO_ENCRYPTION = True
MESSAGE_RETENTION_DAYS = 30
INACTIVE_ACCOUNT_DAYS = 90

# Moderation Settings
ENABLE_CONTENT_FILTERING = True
MAX_WARNINGS_BEFORE_BAN = 3
MODERATION_REVIEW_THRESHOLD = 2  # Number of reports before admin review

# Path Settings
TRANSLATION_PATH = Path(__file__).parent / "translations"
RESOURCES_PATH = Path(__file__).parent / "resources"
