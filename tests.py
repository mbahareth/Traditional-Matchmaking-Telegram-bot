"""
Test script for the Traditional Matchmaking Telegram Bot.
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.models import User, Profile, Match, Conversation, Gender, ReligiosityLevel, CoveringStyle
from src.matching import (
    calculate_personality_compatibility, calculate_zodiac_compatibility,
    calculate_religious_compatibility, calculate_family_values_compatibility,
    calculate_lifestyle_compatibility, calculate_overall_compatibility,
    score_personality_test, determine_zodiac_sign
)
from src.translations import get_text, load_translations
from datetime import datetime

class TestMatchingAlgorithms(unittest.TestCase):
    """Test cases for matching algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock user profiles
        self.user_a = MagicMock(spec=Profile)
        self.user_a.personality_type = "INTJ"
        self.user_a.zodiac_sign = "Aries"
        self.user_a.religiosity_level = ReligiosityLevel.MODERATE
        self.user_a.prayer_habits = "Five times daily"
        self.user_a.religious_education = "Self-taught"
        self.user_a.religious_practices = ["Regular Quran reading", "Islamic charity work"]
        self.user_a.living_arrangement = "Independent home near family"
        self.user_a.family_size = "3-5 children"
        self.user_a.role_expectations = {
            "husband_role": ["Provider", "Spiritual leader"],
            "wife_role": ["Homemaker", "Child-rearer", "Supportive partner"]
        }
        self.user_a.education_level = "Bachelor's Degree"
        self.user_a.interests = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
        
        self.user_b = MagicMock(spec=Profile)
        self.user_b.personality_type = "ENFP"
        self.user_b.zodiac_sign = "Leo"
        self.user_b.religiosity_level = ReligiosityLevel.MODERATE
        self.user_b.prayer_habits = "Most daily prayers"
        self.user_b.religious_education = "Regular Islamic classes"
        self.user_b.religious_practices = ["Regular Quran reading", "Attend religious gatherings"]
        self.user_b.living_arrangement = "Independent home near family"
        self.user_b.family_size = "3-5 children"
        self.user_b.role_expectations = {
            "husband_role": ["Provider", "Spiritual leader", "Decision maker"],
            "wife_role": ["Homemaker", "Child-rearer", "Career professional"]
        }
        self.user_b.education_level = "Master's Degree"
        self.user_b.interests = [MagicMock(id=2), MagicMock(id=3), MagicMock(id=4)]
    
    def test_personality_compatibility(self):
        """Test personality compatibility calculation."""
        score = calculate_personality_compatibility("INTJ", "ENFP")
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_zodiac_compatibility(self):
        """Test zodiac compatibility calculation."""
        score = calculate_zodiac_compatibility("Aries", "Leo")
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_religious_compatibility(self):
        """Test religious compatibility calculation."""
        score = calculate_religious_compatibility(self.user_a, self.user_b)
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_family_values_compatibility(self):
        """Test family values compatibility calculation."""
        score = calculate_family_values_compatibility(self.user_a, self.user_b)
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_lifestyle_compatibility(self):
        """Test lifestyle compatibility calculation."""
        score = calculate_lifestyle_compatibility(self.user_a, self.user_b)
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_overall_compatibility(self):
        """Test overall compatibility calculation."""
        score = calculate_overall_compatibility(self.user_a, self.user_b)
        self.assertIsInstance(score, (int, float))
        self.assertTrue(0 <= score <= 100)
    
    def test_personality_test_scoring(self):
        """Test personality test scoring."""
        # Mock answers to personality test
        answers = {
            'q1': 4,  # Strongly agree (I)
            'q2': 2,  # Disagree (E)
            'q3': 5,  # Strongly agree (I)
            'q4': 1,  # Strongly disagree (E)
            'q5': 4,  # Agree (I)
            'q6': 2,  # Disagree (E)
            'q7': 4,  # Agree (S)
            'q8': 2,  # Disagree (N)
            'q9': 5,  # Strongly agree (S)
            'q10': 1, # Strongly disagree (N)
            'q11': 4, # Agree (S)
            'q12': 2, # Disagree (N)
            'q13': 4, # Agree (T)
            'q14': 2, # Disagree (F)
            'q15': 5, # Strongly agree (T)
            'q16': 1, # Strongly disagree (F)
            'q17': 4, # Agree (T)
            'q18': 2, # Disagree (F)
            'q19': 4, # Agree (J)
            'q20': 2, # Disagree (P)
            'q21': 5, # Strongly agree (J)
            'q22': 1, # Strongly disagree (P)
            'q23': 4, # Agree (J)
            'q24': 2  # Disagree (P)
        }
        
        result = score_personality_test(answers)
        self.assertIn('type', result)
        self.assertIn('scores', result)
        self.assertIn('percentages', result)
        self.assertEqual(len(result['type']), 4)  # MBTI type has 4 letters
    
    def test_zodiac_sign_determination(self):
        """Test zodiac sign determination."""
        # Test a few dates
        aries_date = datetime(2000, 4, 10).date()
        taurus_date = datetime(2000, 5, 1).date()
        gemini_date = datetime(2000, 6, 1).date()
        
        self.assertEqual(determine_zodiac_sign(aries_date).value, "Aries")
        self.assertEqual(determine_zodiac_sign(taurus_date).value, "Taurus")
        self.assertEqual(determine_zodiac_sign(gemini_date).value, "Gemini")

class TestTranslations(unittest.TestCase):
    """Test cases for translations."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Load translations
        load_translations()
    
    def test_get_text(self):
        """Test getting translated text."""
        # Test English translation
        english_text = get_text("welcome_message", lang="en")
        self.assertIsInstance(english_text, str)
        self.assertGreater(len(english_text), 0)
        
        # Test Arabic translation
        arabic_text = get_text("welcome_message", lang="ar")
        self.assertIsInstance(arabic_text, str)
        self.assertGreater(len(arabic_text), 0)
        
        # Create a mock translation for testing formatting
        from src.translations import translations
        if 'en' not in translations:
            translations['en'] = {}
        translations['en']['compatibility_score'] = "Compatibility Score: {score}%"
        
        # Test with formatting
        formatted_text = get_text("compatibility_score", lang="en", score=85)
        self.assertIn("85", formatted_text)
    
    def test_fallback_to_default(self):
        """Test fallback to default language."""
        # Test with non-existent language
        text = get_text("welcome_message", lang="fr")
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)
        
        # Test with non-existent key
        text = get_text("non_existent_key", lang="en")
        self.assertEqual(text, "non_existent_key")

if __name__ == "__main__":
    unittest.main()
