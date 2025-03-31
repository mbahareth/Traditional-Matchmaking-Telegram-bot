# User Profile Structure

## Basic Information
- **name**: String (first name or partial name for privacy)
- **age**: Integer
- **gender**: String (male/female)
- **nationality**: String (Saudi Arabia, UAE, Qatar, Bahrain, Kuwait, Oman)
- **city**: String
- **education_level**: String (High School, Bachelor's, Master's, PhD)
- **profession**: String
- **family_background**: String (optional, tribal affiliation)

## Religious Information
- **religious_commitment**: String (Very committed, Moderately committed, Somewhat committed)
- **prayer_habits**: String (Five times daily, Occasionally, Rarely)
- **religious_education**: String (Formal Islamic education, Self-taught, Basic knowledge)
- **religious_practices**: Array of Strings (Hijab, Beard, etc.)

## Marriage Preferences
- **marriage_timeline**: String (Within 6 months, 6-12 months, 1-2 years)
- **living_arrangement**: String (Separate home, With husband's family, With wife's family)
- **role_expectations**: Object
  - **husband_role**: Array of Strings (Primary provider, Equal partnership, etc.)
  - **wife_role**: Array of Strings (Homemaker, Working professional, etc.)
- **family_size**: String (No children, 1-2 children, 3-5 children, More than 5)

## Personal Interests
- **hobbies**: Array of Strings
- **reading_interests**: Array of Strings
- **travel_experience**: Array of Strings
- **life_goals**: Array of Strings

## Family Involvement
- **family_approval_required**: Boolean
- **family_contacts**: Array of Objects
  - **relation**: String (Father, Mother, Brother, Uncle, etc.)
  - **telegram_id**: String (optional)

## Privacy Settings
- **profile_visibility**: String (All users, Matched users only, After approval)
- **photo_visibility**: String (No photo, Family only, Matched users only)
- **blocked_users**: Array of Strings (user IDs)
- **hidden_from**: Array of Strings (user IDs)

## Verification Status
- **verified**: Boolean
- **verification_level**: String (None, Basic, Professional, Full)
- **verification_documents**: Array of Strings (document references, admin-only access)

## Matching Preferences
- **age_range**: Object
  - **min**: Integer
  - **max**: Integer
- **preferred_nationalities**: Array of Strings
- **preferred_education**: Array of Strings
- **preferred_professions**: Array of Strings
- **distance_preference**: Integer (maximum distance in km)
- **religious_compatibility_importance**: Integer (1-5 scale)
- **family_background_importance**: Integer (1-5 scale)

## Communication Preferences
- **initial_contact_method**: String (Structured questions, Family-supervised, Direct with guidelines)
- **response_time**: String (Within hours, Within a day, Within a week)
- **communication_style**: String (Formal, Semi-formal, Casual but respectful)
- **language_preference**: Array of Strings (Arabic, English, etc.)

## System Data
- **user_id**: String
- **creation_date**: Timestamp
- **last_active**: Timestamp
- **account_status**: String (Active, Suspended, Deactivated)
- **reported_count**: Integer
- **warning_count**: Integer
- **success_stories**: Array of Objects (if applicable)
  - **outcome**: String (Meeting, Engagement, Marriage)
  - **date**: Timestamp
  - **partner_id**: String
