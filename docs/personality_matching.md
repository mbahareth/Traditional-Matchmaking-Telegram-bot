# Personality Assessment and Matching Algorithm

This document outlines the implementation details for the personality assessment features and matching algorithms for the semi-dating Telegram bot.

## 16 Personalities Test Implementation

### Question Set
The bot will implement an abbreviated version of the Myers-Briggs Type Indicator (MBTI) assessment with 24 questions, focusing on the four key dimensions:

1. **Extraversion (E) vs. Introversion (I)** - 6 questions
   - How you gain energy and interact with the world

2. **Sensing (S) vs. Intuition (N)** - 6 questions
   - How you process information and perceive the world

3. **Thinking (T) vs. Feeling (F)** - 6 questions
   - How you make decisions and form judgments

4. **Judging (J) vs. Perceiving (P)** - 6 questions
   - How you approach structure, planning, and decision-making

### Sample Questions
1. "You prefer spending time with a small group of close friends rather than at large social gatherings."
2. "You often focus more on details than the big picture."
3. "When making decisions, you typically prioritize logic over personal feelings."
4. "You prefer having a detailed plan rather than being spontaneous."

### Scoring System
- Each question will be answered on a 5-point scale (Strongly Disagree to Strongly Agree)
- Scores will be calculated for each dimension (E/I, S/N, T/F, J/P)
- The higher score in each pair determines the personality type letter
- Results in one of 16 personality types (INTJ, ENFP, etc.)

### Compatibility Matching
The algorithm will use established MBTI compatibility patterns:
- Complementary functions (e.g., Thinking pairs well with Feeling)
- Shared values but different approaches (e.g., INFJ and ENFP)
- Similar communication styles
- Balancing strengths and weaknesses

## Horoscope Integration

### Data Collection
- Birth date (required)
- Birth time (optional, for more detailed analysis)
- Birth location (optional, for rising sign calculation)

### Zodiac Systems
1. **Western Zodiac**
   - 12 signs based on solar calendar
   - Compatibility based on traditional element relationships (Fire, Earth, Air, Water)

2. **Islamic/Arabic Astrological Elements**
   - Integration of traditional Islamic lunar calendar considerations
   - Culturally appropriate interpretations

### Compatibility Calculation
- Element compatibility (Fire, Earth, Air, Water)
- Complementary sign relationships
- Planetary ruler harmonies
- House position considerations (if birth time provided)

### Cultural Sensitivity
- Clear framing as an optional feature
- Religious context explanation
- Disable option for users who prefer not to use this feature
- Educational content on historical context in Islamic culture

## Enhanced Profile Questions for Algorithm

### Religious Dimension
```json
{
  "religiosity_level": {
    "type": "single_choice",
    "options": ["Conservative/Traditional", "Moderate", "Progressive/Liberal"],
    "weight": 10
  },
  "prayer_frequency": {
    "type": "single_choice",
    "options": ["Five times daily", "Most daily prayers", "Weekly (Jummah)", "Occasionally", "Rarely"],
    "weight": 8
  },
  "religious_education": {
    "type": "single_choice",
    "options": ["Formal Islamic education", "Regular Islamic classes", "Self-taught", "Basic knowledge"],
    "weight": 6
  },
  "religious_practices": {
    "type": "multiple_choice",
    "options": ["Regular Quran reading", "Attend religious gatherings", "Islamic charity work", "Religious fasting beyond Ramadan"],
    "weight": 7
  }
}
```

### Covering Preferences
```json
{
  "personal_covering": {
    "type": "single_choice",
    "options": ["Face covering (niqab)", "Hair covering only (hijab)", "Natural with no covers", "Situational covering"],
    "weight": 9
  },
  "partner_covering_preference": {
    "type": "single_choice",
    "options": ["Face covering (niqab)", "Hair covering only (hijab)", "Natural with no covers", "No preference"],
    "weight": 8
  },
  "covering_importance": {
    "type": "scale",
    "range": [1, 5],
    "description": "How important is this preference to you?",
    "weight": 7
  }
}
```

### Family Values
```json
{
  "living_arrangement": {
    "type": "single_choice",
    "options": ["With husband's family", "With wife's family", "Independent home near family", "Completely independent"],
    "weight": 9
  },
  "family_visits": {
    "type": "single_choice",
    "options": ["Daily", "Several times weekly", "Weekly", "Monthly", "Occasionally"],
    "weight": 6
  },
  "family_decision_making": {
    "type": "single_choice",
    "options": ["Traditional (male-led)", "Consultative", "Equal partnership", "Situational"],
    "weight": 8
  }
}
```

### Lifestyle Choices
```json
{
  "dietary_preferences": {
    "type": "multiple_choice",
    "options": ["Strict halal only", "Halal at home only", "Vegetarian", "No restrictions"],
    "weight": 7
  },
  "travel_interests": {
    "type": "multiple_choice",
    "options": ["Islamic historical sites", "Nature destinations", "International travel", "Local travel only"],
    "weight": 5
  },
  "entertainment": {
    "type": "multiple_choice",
    "options": ["Religious content only", "Family-friendly content", "Mainstream media", "Art and culture"],
    "weight": 6
  },
  "social_media": {
    "type": "single_choice",
    "options": ["Very active", "Moderately active", "Minimal usage", "No social media"],
    "weight": 4
  }
}
```

## Matching Algorithm Implementation

### Compatibility Score Calculation
```python
def calculate_compatibility(user_a, user_b):
    # Base score
    total_score = 0
    max_possible_score = 0
    
    # Religious compatibility (30%)
    religious_score = compare_religious_values(user_a, user_b)
    total_score += religious_score * 0.3
    max_possible_score += 100 * 0.3
    
    # Personality compatibility (25%)
    if both_users_completed_personality_test(user_a, user_b):
        personality_score = compare_personality_types(user_a, user_b)
        total_score += personality_score * 0.25
        max_possible_score += 100 * 0.25
    
    # Family values alignment (20%)
    family_score = compare_family_values(user_a, user_b)
    total_score += family_score * 0.2
    max_possible_score += 100 * 0.2
    
    # Lifestyle compatibility (15%)
    lifestyle_score = compare_lifestyle(user_a, user_b)
    total_score += lifestyle_score * 0.15
    max_possible_score += 100 * 0.15
    
    # Horoscope compatibility (10%, if enabled)
    if both_users_enabled_horoscope(user_a, user_b):
        horoscope_score = compare_horoscope(user_a, user_b)
        total_score += horoscope_score * 0.1
        max_possible_score += 100 * 0.1
    
    # Normalize to 100%
    final_score = (total_score / max_possible_score) * 100
    
    # Check for deal-breakers
    if has_dealbreakers(user_a, user_b):
        final_score = 0
    
    return final_score
```

### Deal-Breaker Implementation
```python
def has_dealbreakers(user_a, user_b):
    # Religious level incompatibility
    if abs(religiosity_level_value(user_a) - religiosity_level_value(user_b)) > 1:
        return True
    
    # Covering preference mismatch
    if user_a.covering_preference != "No preference" and user_a.covering_preference != user_b.personal_covering:
        if user_a.covering_importance > 4:  # High importance
            return True
    
    # Family living arrangement conflict
    if user_a.living_arrangement != user_b.living_arrangement:
        if user_a.living_arrangement_importance > 4 or user_b.living_arrangement_importance > 4:
            return True
    
    # Custom user-defined deal-breakers
    for dealbreaker in user_a.dealbreakers:
        if not matches_preference(dealbreaker, user_b):
            return True
    
    return False
```

### Weighted Preference System
Each preference will have an importance rating (1-5) that affects its weight in the matching algorithm. Users can mark certain preferences as deal-breakers, which will filter out incompatible matches entirely.

### Machine Learning Enhancement Plan
1. **Data Collection Phase**
   - Store interaction outcomes (matches, conversations, user feedback)
   - Track successful vs. unsuccessful matches

2. **Pattern Recognition**
   - Identify common factors in successful matches
   - Detect patterns that predict compatibility

3. **Algorithm Refinement**
   - Adjust weighting based on success patterns
   - Personalize algorithm based on user feedback
   - Implement A/B testing for algorithm improvements

4. **Implementation Timeline**
   - Initial static algorithm at launch
   - Data collection for first 3 months
   - First ML enhancement at 6-month mark
   - Continuous improvement thereafter

## Arabic Translation Integration

### Translation Management
- All personality questions will be available in both English and Arabic
- Results and interpretations will be culturally adapted, not just translated
- Dialect considerations for Gulf Arabic speakers
- Religious terminology will be reviewed by cultural experts

### Bilingual Implementation
```python
personality_questions = {
    "q1": {
        "en": "You prefer spending time with a small group of close friends rather than at large social gatherings.",
        "ar": "تفضل قضاء الوقت مع مجموعة صغيرة من الأصدقاء المقربين بدلاً من التجمعات الاجتماعية الكبيرة."
    },
    "q2": {
        "en": "You often focus more on details than the big picture.",
        "ar": "غالبًا ما تركز على التفاصيل أكثر من الصورة الكبيرة."
    },
    # Additional questions...
}

personality_types = {
    "INTJ": {
        "en": "Architect: Strategic, innovative thinker with a plan for everything",
        "ar": "المهندس: مفكر استراتيجي مبتكر لديه خطة لكل شيء"
    },
    "ENFP": {
        "en": "Campaigner: Enthusiastic, creative, sociable free spirit who finds potential in every opportunity",
        "ar": "المناصر: روح حرة متحمسة ومبدعة واجتماعية تجد إمكانات في كل فرصة"
    },
    # Additional types...
}
```

## Implementation Roadmap

1. **Database Schema Updates**
   - Add personality assessment fields
   - Add horoscope data fields
   - Add enhanced religious and covering preference fields

2. **Assessment Implementation**
   - Develop personality test module
   - Implement horoscope calculation system
   - Create enhanced profile questionnaires

3. **Algorithm Development**
   - Implement compatibility scoring system
   - Develop deal-breaker filtering
   - Create weighted preference system

4. **Translation Integration**
   - Implement translation management system
   - Develop language toggle functionality
   - Create bilingual content for all assessments

5. **Testing and Validation**
   - Verify cultural appropriateness
   - Test compatibility algorithm with sample profiles
   - Validate translation accuracy and cultural sensitivity
