"""
Personality matching algorithms for the Traditional Matchmaking Telegram Bot.
"""

import math
from enum import Enum

class PersonalityType(Enum):
    """MBTI Personality Types"""
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"

class ZodiacSign(Enum):
    """Western Zodiac Signs"""
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

# MBTI Compatibility Matrix (0-100 scale)
# Based on complementary cognitive functions and observed compatibility patterns
MBTI_COMPATIBILITY = {
    PersonalityType.INTJ: {
        PersonalityType.INTJ: 65, PersonalityType.INTP: 75, PersonalityType.ENTJ: 80, PersonalityType.ENTP: 85,
        PersonalityType.INFJ: 70, PersonalityType.INFP: 65, PersonalityType.ENFJ: 75, PersonalityType.ENFP: 85,
        PersonalityType.ISTJ: 60, PersonalityType.ISFJ: 55, PersonalityType.ESTJ: 65, PersonalityType.ESFJ: 50,
        PersonalityType.ISTP: 70, PersonalityType.ISFP: 60, PersonalityType.ESTP: 65, PersonalityType.ESFP: 55
    },
    PersonalityType.INTP: {
        PersonalityType.INTJ: 75, PersonalityType.INTP: 65, PersonalityType.ENTJ: 85, PersonalityType.ENTP: 80,
        PersonalityType.INFJ: 75, PersonalityType.INFP: 70, PersonalityType.ENFJ: 85, PersonalityType.ENFP: 75,
        PersonalityType.ISTJ: 65, PersonalityType.ISFJ: 60, PersonalityType.ESTJ: 70, PersonalityType.ESFJ: 55,
        PersonalityType.ISTP: 75, PersonalityType.ISFP: 65, PersonalityType.ESTP: 70, PersonalityType.ESFP: 60
    },
    # Additional personality types omitted for brevity
}

# Zodiac Compatibility Matrix (0-100 scale)
# Based on traditional astrological compatibility between elements and qualities
ZODIAC_COMPATIBILITY = {
    ZodiacSign.ARIES: {
        ZodiacSign.ARIES: 70, ZodiacSign.TAURUS: 55, ZodiacSign.GEMINI: 75, ZodiacSign.CANCER: 60,
        ZodiacSign.LEO: 90, ZodiacSign.VIRGO: 65, ZodiacSign.LIBRA: 80, ZodiacSign.SCORPIO: 60,
        ZodiacSign.SAGITTARIUS: 85, ZodiacSign.CAPRICORN: 55, ZodiacSign.AQUARIUS: 75, ZodiacSign.PISCES: 65
    },
    ZodiacSign.TAURUS: {
        ZodiacSign.ARIES: 55, ZodiacSign.TAURUS: 75, ZodiacSign.GEMINI: 60, ZodiacSign.CANCER: 85,
        ZodiacSign.LEO: 65, ZodiacSign.VIRGO: 90, ZodiacSign.LIBRA: 70, ZodiacSign.SCORPIO: 85,
        ZodiacSign.SAGITTARIUS: 55, ZodiacSign.CAPRICORN: 90, ZodiacSign.AQUARIUS: 60, ZodiacSign.PISCES: 80
    },
    # Additional zodiac signs omitted for brevity
}

def calculate_personality_compatibility(personality_type_a, personality_type_b):
    """
    Calculate compatibility score between two MBTI personality types.
    
    Args:
        personality_type_a: MBTI type of first person (string or PersonalityType enum)
        personality_type_b: MBTI type of second person (string or PersonalityType enum)
        
    Returns:
        Compatibility score (0-100)
    """
    # Convert string types to enum if needed
    if isinstance(personality_type_a, str):
        personality_type_a = PersonalityType(personality_type_a)
    if isinstance(personality_type_b, str):
        personality_type_b = PersonalityType(personality_type_b)
    
    # Get compatibility score from matrix
    try:
        return MBTI_COMPATIBILITY.get(personality_type_a, {}).get(personality_type_b, 50)
    except Exception:
        # Default to neutral compatibility if types are invalid
        return 50

def calculate_zodiac_compatibility(sign_a, sign_b):
    """
    Calculate compatibility score between two zodiac signs.
    
    Args:
        sign_a: Zodiac sign of first person (string or ZodiacSign enum)
        sign_b: Zodiac sign of second person (string or ZodiacSign enum)
        
    Returns:
        Compatibility score (0-100)
    """
    # Convert string signs to enum if needed
    if isinstance(sign_a, str):
        sign_a = ZodiacSign(sign_a)
    if isinstance(sign_b, str):
        sign_b = ZodiacSign(sign_b)
    
    # Get compatibility score from matrix
    try:
        return ZODIAC_COMPATIBILITY.get(sign_a, {}).get(sign_b, 50)
    except Exception:
        # Default to neutral compatibility if signs are invalid
        return 50

def calculate_religious_compatibility(user_a, user_b):
    """
    Calculate religious compatibility score between two users.
    
    Args:
        user_a: Profile of first user
        user_b: Profile of second user
        
    Returns:
        Compatibility score (0-100)
    """
    score = 0
    max_score = 0
    
    # Religiosity level compatibility
    if user_a.religiosity_level and user_b.religiosity_level:
        religiosity_diff = abs(religiosity_level_value(user_a.religiosity_level) - 
                              religiosity_level_value(user_b.religiosity_level))
        # 0 difference = 100 points, 1 difference = 70 points, 2 difference = 30 points
        religiosity_score = max(0, 100 - (religiosity_diff * 35))
        score += religiosity_score
        max_score += 100
    
    # Prayer habits compatibility
    if user_a.prayer_habits and user_b.prayer_habits:
        prayer_diff = abs(prayer_habits_value(user_a.prayer_habits) - 
                         prayer_habits_value(user_b.prayer_habits))
        # 0 difference = 100 points, 4 difference = 0 points
        prayer_score = max(0, 100 - (prayer_diff * 25))
        score += prayer_score
        max_score += 100
    
    # Religious education compatibility
    if user_a.religious_education and user_b.religious_education:
        education_diff = abs(religious_education_value(user_a.religious_education) - 
                            religious_education_value(user_b.religious_education))
        # 0 difference = 100 points, 3 difference = 0 points
        education_score = max(0, 100 - (education_diff * 33))
        score += education_score
        max_score += 100
    
    # Religious practices overlap
    if user_a.religious_practices and user_b.religious_practices:
        practices_a = set(user_a.religious_practices)
        practices_b = set(user_b.religious_practices)
        
        if practices_a and practices_b:
            overlap = len(practices_a.intersection(practices_b))
            total = len(practices_a.union(practices_b))
            practices_score = (overlap / total) * 100
            score += practices_score
            max_score += 100
    
    # Calculate final score
    return score / max_score * 100 if max_score > 0 else 50

def calculate_family_values_compatibility(user_a, user_b):
    """
    Calculate family values compatibility score between two users.
    
    Args:
        user_a: Profile of first user
        user_b: Profile of second user
        
    Returns:
        Compatibility score (0-100)
    """
    score = 0
    max_score = 0
    
    # Living arrangement compatibility
    if user_a.living_arrangement and user_b.living_arrangement:
        if user_a.living_arrangement == user_b.living_arrangement:
            score += 100
        else:
            # Some arrangements are more compatible than others
            arrangement_compatibility = {
                ("With husband's family", "With husband's family"): 100,
                ("With wife's family", "With wife's family"): 100,
                ("With husband's family", "Independent home near family"): 70,
                ("With wife's family", "Independent home near family"): 70,
                ("Independent home near family", "Independent home near family"): 100,
                ("Completely independent", "Completely independent"): 100,
                ("Independent home near family", "Completely independent"): 80,
                ("With husband's family", "With wife's family"): 40,
                ("With husband's family", "Completely independent"): 50,
                ("With wife's family", "Completely independent"): 50
            }
            
            arrangement_pair = (user_a.living_arrangement, user_b.living_arrangement)
            reverse_pair = (user_b.living_arrangement, user_a.living_arrangement)
            
            if arrangement_pair in arrangement_compatibility:
                score += arrangement_compatibility[arrangement_pair]
            elif reverse_pair in arrangement_compatibility:
                score += arrangement_compatibility[reverse_pair]
            else:
                score += 50  # Default compatibility
        
        max_score += 100
    
    # Family size compatibility
    if user_a.family_size and user_b.family_size:
        family_size_diff = abs(family_size_value(user_a.family_size) - 
                              family_size_value(user_b.family_size))
        # 0 difference = 100 points, 3 difference = 0 points
        family_size_score = max(0, 100 - (family_size_diff * 33))
        score += family_size_score
        max_score += 100
    
    # Role expectations compatibility
    if (user_a.role_expectations and user_b.role_expectations and
        'husband_role' in user_a.role_expectations and 'wife_role' in user_a.role_expectations and
        'husband_role' in user_b.role_expectations and 'wife_role' in user_b.role_expectations):
        
        # Compare expectations for husband role
        husband_role_a = set(user_a.role_expectations['husband_role'])
        husband_role_b = set(user_b.role_expectations['husband_role'])
        husband_overlap = len(husband_role_a.intersection(husband_role_b))
        husband_total = len(husband_role_a.union(husband_role_b))
        husband_score = (husband_overlap / husband_total) * 100 if husband_total > 0 else 50
        
        # Compare expectations for wife role
        wife_role_a = set(user_a.role_expectations['wife_role'])
        wife_role_b = set(user_b.role_expectations['wife_role'])
        wife_overlap = len(wife_role_a.intersection(wife_role_b))
        wife_total = len(wife_role_a.union(wife_role_b))
        wife_score = (wife_overlap / wife_total) * 100 if wife_total > 0 else 50
        
        # Average the scores
        role_score = (husband_score + wife_score) / 2
        score += role_score
        max_score += 100
    
    # Calculate final score
    return score / max_score * 100 if max_score > 0 else 50

def calculate_lifestyle_compatibility(user_a, user_b):
    """
    Calculate lifestyle compatibility score between two users.
    
    Args:
        user_a: Profile of first user
        user_b: Profile of second user
        
    Returns:
        Compatibility score (0-100)
    """
    score = 0
    max_score = 0
    
    # Education level compatibility
    if user_a.education_level and user_b.education_level:
        education_diff = abs(education_level_value(user_a.education_level) - 
                            education_level_value(user_b.education_level))
        # 0 difference = 100 points, 4 difference = 0 points
        education_score = max(0, 100 - (education_diff * 25))
        score += education_score
        max_score += 100
    
    # Interests overlap
    if user_a.interests and user_b.interests:
        interests_a = set(interest.id for interest in user_a.interests)
        interests_b = set(interest.id for interest in user_b.interests)
        
        if interests_a and interests_b:
            overlap = len(interests_a.intersection(interests_b))
            total = len(interests_a.union(interests_b))
            interests_score = (overlap / total) * 100
            score += interests_score
            max_score += 100
    
    # Calculate final score
    return score / max_score * 100 if max_score > 0 else 50

def calculate_overall_compatibility(user_a, user_b, weights=None):
    """
    Calculate overall compatibility score between two users.
    
    Args:
        user_a: Profile of first user
        user_b: Profile of second user
        weights: Dictionary of weights for different compatibility factors
        
    Returns:
        Overall compatibility score (0-100)
    """
    from src.config import (
        RELIGIOUS_COMPATIBILITY_WEIGHT,
        PERSONALITY_COMPATIBILITY_WEIGHT,
        FAMILY_VALUES_WEIGHT,
        LIFESTYLE_COMPATIBILITY_WEIGHT,
        HOROSCOPE_COMPATIBILITY_WEIGHT
    )
    
    # Use default weights if not provided
    if weights is None:
        weights = {
            'religious': RELIGIOUS_COMPATIBILITY_WEIGHT,
            'personality': PERSONALITY_COMPATIBILITY_WEIGHT,
            'family': FAMILY_VALUES_WEIGHT,
            'lifestyle': LIFESTYLE_COMPATIBILITY_WEIGHT,
            'horoscope': HOROSCOPE_COMPATIBILITY_WEIGHT
        }
    
    # Calculate individual compatibility scores
    religious_score = calculate_religious_compatibility(user_a, user_b)
    family_score = calculate_family_values_compatibility(user_a, user_b)
    lifestyle_score = calculate_lifestyle_compatibility(user_a, user_b)
    
    # Calculate personality score if both users have completed the test
    personality_score = 50  # Default neutral score
    if user_a.personality_type and user_b.personality_type:
        personality_score = calculate_personality_compatibility(
            user_a.personality_type, user_b.personality_type
        )
    
    # Calculate horoscope score if both users have provided birth information
    horoscope_score = 50  # Default neutral score
    if user_a.zodiac_sign and user_b.zodiac_sign:
        horoscope_score = calculate_zodiac_compatibility(
            user_a.zodiac_sign, user_b.zodiac_sign
        )
    
    # Calculate weighted average
    total_score = (
        religious_score * weights['religious'] +
        personality_score * weights['personality'] +
        family_score * weights['family'] +
        lifestyle_score * weights['lifestyle'] +
        horoscope_score * weights['horoscope']
    )
    
    # Check for deal-breakers
    if has_dealbreakers(user_a, user_b):
        return 0
    
    return total_score

def has_dealbreakers(user_a, user_b):
    """
    Check if there are any deal-breakers between two users.
    
    Args:
        user_a: Profile of first user
        user_b: Profile of second user
        
    Returns:
        True if there are deal-breakers, False otherwise
    """
    # Religious level incompatibility
    if (user_a.religiosity_level and user_b.religiosity_level and
        abs(religiosity_level_value(user_a.religiosity_level) - 
            religiosity_level_value(user_b.religiosity_level)) > 1):
        
        # Check if this is a high-importance factor for either user
        if (hasattr(user_a, 'settings') and user_a.settings and 
            user_a.settings.religious_compatibility_importance > 4):
            return True
        
        if (hasattr(user_b, 'settings') and user_b.settings and 
            user_b.settings.religious_compatibility_importance > 4):
            return True
    
    # Covering preference mismatch (for male-female matches)
    try:
        if (user_a.gender != user_b.gender and  # Only check for opposite gender matches
            hasattr(user_a, 'partner_covering_preference') and user_a.partner_covering_preference and
            hasattr(user_b, 'personal_covering') and user_b.personal_covering and
            user_a.partner_covering_preference != user_b.personal_covering and
            hasattr(user_a, 'covering_importance') and 
            (isinstance(user_a.covering_importance, int) and user_a.covering_importance > 4)):
            return True
        
        if (user_a.gender != user_b.gender and  # Only check for opposite gender matches
            hasattr(user_b, 'partner_covering_preference') and user_b.partner_covering_preference and
            hasattr(user_a, 'personal_covering') and user_a.personal_covering and
            user_b.partner_covering_preference != user_a.personal_covering and
            hasattr(user_b, 'covering_importance') and 
            (isinstance(user_b.covering_importance, int) and user_b.covering_importance > 4)):
            return True
    except (TypeError, AttributeError):
        # If there's any error in comparison, don't treat it as a dealbreaker
        pass
    
    return False

# Helper functions for value conversion

def religiosity_level_value(level):
    """Convert religiosity level to numeric value."""
    values = {
        "conservative": 2,
        "moderate": 1,
        "progressive": 0
    }
    return values.get(level.lower() if isinstance(level, str) else level.value.lower(), 1)

def prayer_habits_value(habits):
    """Convert prayer habits to numeric value."""
    values = {
        "five times daily": 4,
        "most daily prayers": 3,
        "weekly": 2,
        "occasionally": 1,
        "rarely": 0
    }
    return values.get(habits.lower() if isinstance(habits, str) else habits.value.lower(), 2)

def religious_education_value(education):
    """Convert religious education to numeric value."""
    values = {
        "formal islamic education": 3,
        "regular islamic classes": 2,
        "self-taught": 1,
        "basic knowledge": 0
    }
    return values.get(education.lower() if isinstance(education, str) else education.value.lower(), 1)

def family_size_value(size):
    """Convert family size preference to numeric value."""
    values = {
        "no children": 0,
        "1-2 children": 1,
        "3-5 children": 2,
        "more than 5": 3
    }
    return values.get(size.lower() if isinstance(size, str) else size.value.lower(), 1)

def education_level_value(level):
    """Convert education level to numeric value."""
    values = {
        "high school": 0,
        "bachelor's": 1,
        "bachelor's degree": 1,
        "master's": 2,
        "master's degree": 2,
        "phd": 3,
        "doctorate": 3,
        "other": 0
    }
    return values.get(level.lower() if isinstance(level, str) else level.value.lower(), 0)

# Personality test scoring functions

def score_personality_test(answers):
    """
    Score the personality test and determine MBTI type.
    
    Args:
        answers: Dictionary of question IDs and responses (1-5 scale)
        
    Returns:
        Dictionary with personality type and detailed scores
    """
    # Initialize scores for each dimension
    scores = {
        'E': 0, 'I': 0,  # Extraversion vs. Introversion
        'S': 0, 'N': 0,  # Sensing vs. Intuition
        'T': 0, 'F': 0,  # Thinking vs. Feeling
        'J': 0, 'P': 0   # Judging vs. Perceiving
    }
    
    # Question mappings to dimensions
    question_mappings = {
        # E/I questions (1-6)
        'q1': {'dimension': 'I', 'reverse': False},
        'q2': {'dimension': 'E', 'reverse': False},
        'q3': {'dimension': 'I', 'reverse': False},
        'q4': {'dimension': 'E', 'reverse': False},
        'q5': {'dimension': 'I', 'reverse': False},
        'q6': {'dimension': 'E', 'reverse': False},
        
        # S/N questions (7-12)
        'q7': {'dimension': 'S', 'reverse': False},
        'q8': {'dimension': 'N', 'reverse': False},
        'q9': {'dimension': 'S', 'reverse': False},
        'q10': {'dimension': 'N', 'reverse': False},
        'q11': {'dimension': 'S', 'reverse': False},
        'q12': {'dimension': 'N', 'reverse': False},
        
        # T/F questions (13-18)
        'q13': {'dimension': 'T', 'reverse': False},
        'q14': {'dimension': 'F', 'reverse': False},
        'q15': {'dimension': 'T', 'reverse': False},
        'q16': {'dimension': 'F', 'reverse': False},
        'q17': {'dimension': 'T', 'reverse': False},
        'q18': {'dimension': 'F', 'reverse': False},
        
        # J/P questions (19-24)
        'q19': {'dimension': 'J', 'reverse': False},
        'q20': {'dimension': 'P', 'reverse': False},
        'q21': {'dimension': 'J', 'reverse': False},
        'q22': {'dimension': 'P', 'reverse': False},
        'q23': {'dimension': 'J', 'reverse': False},
        'q24': {'dimension': 'P', 'reverse': False}
    }
    
    # Process each answer
    for question_id, answer in answers.items():
        if question_id in question_mappings:
            mapping = question_mappings[question_id]
            dimension = mapping['dimension']
            
            # Convert 1-5 scale to 0-4 scale
            value = answer - 1
            
            # Reverse score if needed
            if mapping['reverse']:
                value = 4 - value
            
            # Add to dimension score
            scores[dimension] += value
    
    # Determine type based on higher score in each dimension pair
    personality_type = ''
    personality_type += 'E' if scores['E'] >= scores['I'] else 'I'
    personality_type += 'S' if scores['S'] >= scores['N'] else 'N'
    personality_type += 'T' if scores['T'] >= scores['F'] else 'F'
    personality_type += 'J' if scores['J'] >= scores['P'] else 'P'
    
    # Calculate dimension percentages
    total_questions = 6  # 6 questions per dimension
    max_score = total_questions * 4  # Maximum possible score per dimension (0-4 scale)
    
    percentages = {
        'E': (scores['E'] / max_score) * 100,
        'I': (scores['I'] / max_score) * 100,
        'S': (scores['S'] / max_score) * 100,
        'N': (scores['N'] / max_score) * 100,
        'T': (scores['T'] / max_score) * 100,
        'F': (scores['F'] / max_score) * 100,
        'J': (scores['J'] / max_score) * 100,
        'P': (scores['P'] / max_score) * 100
    }
    
    return {
        'type': personality_type,
        'scores': scores,
        'percentages': percentages
    }

def determine_zodiac_sign(birth_date):
    """
    Determine Western zodiac sign based on birth date.
    
    Args:
        birth_date: datetime.date object
        
    Returns:
        ZodiacSign enum
    """
    month = birth_date.month
    day = birth_date.day
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return ZodiacSign.ARIES
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return ZodiacSign.TAURUS
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return ZodiacSign.GEMINI
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return ZodiacSign.CANCER
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return ZodiacSign.LEO
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return ZodiacSign.VIRGO
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return ZodiacSign.LIBRA
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return ZodiacSign.SCORPIO
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return ZodiacSign.SAGITTARIUS
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return ZodiacSign.CAPRICORN
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return ZodiacSign.AQUARIUS
    else:
        return ZodiacSign.PISCES
