"""
Translation utilities for the Traditional Matchmaking Telegram Bot.
"""

import json
import os
from pathlib import Path

from src.config import TRANSLATION_PATH, DEFAULT_LANGUAGE

# Create translations directory if it doesn't exist
os.makedirs(TRANSLATION_PATH, exist_ok=True)

# Initialize translations dictionary
translations = {}

def load_translations():
    """Load all translation files from the translations directory."""
    global translations
    translations = {}
    
    # Ensure the translations directory exists
    if not os.path.exists(TRANSLATION_PATH):
        os.makedirs(TRANSLATION_PATH)
        # Create default translation files
        create_default_translation_files()
    
    # Load all JSON files in the translations directory
    for file_path in TRANSLATION_PATH.glob('*.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lang_code = file_path.stem
                translations[lang_code] = json.load(f)
        except Exception as e:
            print(f"Error loading translation file {file_path}: {e}")

def create_default_translation_files():
    """Create default English and Arabic translation files."""
    # English translations
    en_translations = {
        "welcome_message": "Welcome to the Traditional Matchmaking Bot for Saudi Arabia and GCC nationals. This service is designed to help you find a suitable marriage partner while respecting cultural and religious values.",
        "language_selection": "Please select your preferred language:",
        "english": "English",
        "arabic": "العربية",
        "main_menu": "Main Menu",
        "profile_setup": "Profile Setup",
        "view_matches": "View Potential Matches",
        "settings": "Settings",
        "family_involvement": "Family Involvement",
        "conversations": "My Conversations",
        "help": "Help & Support",
        "terms_acceptance": "Before using this service, you must read and accept our Terms and Conditions and Privacy Policy.",
        "accept": "I Accept",
        "decline": "Decline",
        "age_verification": "Are you 18 years of age or older?",
        "yes": "Yes",
        "no": "No",
        "under_18_message": "We're sorry, but you must be 18 years or older to use this service.",
        "basic_info_prompt": "Let's set up your profile. Please provide your basic information.",
        "name_prompt": "What is your name? (First name or partial name for privacy)",
        "age_prompt": "What is your age?",
        "gender_prompt": "What is your gender?",
        "male": "Male",
        "female": "Female",
        "nationality_prompt": "What is your nationality?",
        "city_prompt": "In which city do you live?",
        "education_prompt": "What is your highest level of education?",
        "high_school": "High School",
        "bachelors": "Bachelor's Degree",
        "masters": "Master's Degree",
        "phd": "PhD",
        "other": "Other",
        "profession_prompt": "What is your profession?",
        "religious_info_prompt": "Now, let's add some information about your religious preferences.",
        "religiosity_prompt": "How would you describe your religious observance?",
        "conservative": "Conservative/Traditional",
        "moderate": "Moderate",
        "progressive": "Progressive/Liberal",
        "prayer_habits_prompt": "How often do you pray?",
        "five_times": "Five times daily",
        "most_prayers": "Most daily prayers",
        "weekly": "Weekly (Jummah)",
        "occasionally": "Occasionally",
        "rarely": "Rarely",
        "covering_prompt": "What is your covering style? (For women)",
        "niqab": "Face covering (niqab)",
        "hijab": "Hair covering only (hijab)",
        "none": "Natural with no covers",
        "situational": "Situational covering",
        "match_found": "We found a potential match for you!",
        "compatibility_score": "Compatibility Score: {score}%",
        "interested": "Interested ✓",
        "not_interested": "Not Interested ✗",
        "mutual_match": "Congratulations! You have a new match with {name}. You both expressed interest in each other.",
        "group_created": "A conversation group has been created for you and {name}. May this be the beginning of a blessed connection.",
        "conversation_starters": "Here are some suggested topics to discuss:",
        "topic_1": "Family values and traditions",
        "topic_2": "Life goals and aspirations",
        "topic_3": "Religious practices and beliefs",
        "topic_4": "Expectations for married life",
        "family_invitation": "Would you like to invite a family member to oversee this conversation?",
        "invite_family": "Invite Family Member",
        "later": "Maybe Later",
        "personality_test_intro": "This personality assessment will help us find compatible matches. Please answer honestly.",
        "strongly_disagree": "Strongly Disagree",
        "disagree": "Disagree",
        "neutral": "Neutral",
        "agree": "Agree",
        "strongly_agree": "Strongly Agree",
        "horoscope_intro": "Optional: Provide your birth information for additional compatibility insights.",
        "birth_date_prompt": "What is your birth date?",
        "birth_time_prompt": "What is your birth time? (Optional)",
        "birth_location_prompt": "Where were you born? (Optional)",
        "skip": "Skip this step",
        "profile_complete": "Your profile is complete! We'll start looking for compatible matches for you.",
        "settings_updated": "Your settings have been updated successfully.",
        "error_message": "An error occurred. Please try again later.",
        "report_user": "Report User",
        "block_user": "Block User",
        "report_reason_prompt": "Please select a reason for reporting this user:",
        "inappropriate_behavior": "Inappropriate Behavior",
        "fake_profile": "Fake Profile",
        "harassment": "Harassment",
        "other_reason": "Other",
        "report_submitted": "Your report has been submitted. Thank you for helping keep our community safe.",
        "blocked_user": "You have blocked this user. They will no longer be able to contact you.",
        "success_story_prompt": "Would you like to share your success story with our community?",
        "share": "Share My Story",
        "keep_private": "Keep Private",
        "thank_you": "Thank you for using our service!"
    }
    
    # Arabic translations
    ar_translations = {
        "welcome_message": "مرحبًا بك في روبوت التوفيق التقليدي للسعوديين ومواطني دول مجلس التعاون الخليجي. تم تصميم هذه الخدمة لمساعدتك في العثور على شريك زواج مناسب مع احترام القيم الثقافية والدينية.",
        "language_selection": "يرجى اختيار لغتك المفضلة:",
        "english": "English",
        "arabic": "العربية",
        "main_menu": "القائمة الرئيسية",
        "profile_setup": "إعداد الملف الشخصي",
        "view_matches": "عرض التوافقات المحتملة",
        "settings": "الإعدادات",
        "family_involvement": "مشاركة العائلة",
        "conversations": "محادثاتي",
        "help": "المساعدة والدعم",
        "terms_acceptance": "قبل استخدام هذه الخدمة، يجب عليك قراءة وقبول شروط وأحكام وسياسة الخصوصية الخاصة بنا.",
        "accept": "أوافق",
        "decline": "أرفض",
        "age_verification": "هل عمرك 18 عامًا أو أكثر؟",
        "yes": "نعم",
        "no": "لا",
        "under_18_message": "نأسف، ولكن يجب أن يكون عمرك 18 عامًا أو أكثر لاستخدام هذه الخدمة.",
        "basic_info_prompt": "دعنا نقوم بإعداد ملفك الشخصي. يرجى تقديم معلوماتك الأساسية.",
        "name_prompt": "ما هو اسمك؟ (الاسم الأول أو جزء من الاسم للخصوصية)",
        "age_prompt": "كم عمرك؟",
        "gender_prompt": "ما هو جنسك؟",
        "male": "ذكر",
        "female": "أنثى",
        "nationality_prompt": "ما هي جنسيتك؟",
        "city_prompt": "في أي مدينة تعيش؟",
        "education_prompt": "ما هو أعلى مستوى تعليمي لديك؟",
        "high_school": "الثانوية العامة",
        "bachelors": "بكالوريوس",
        "masters": "ماجستير",
        "phd": "دكتوراه",
        "other": "أخرى",
        "profession_prompt": "ما هي مهنتك؟",
        "religious_info_prompt": "الآن، دعنا نضيف بعض المعلومات حول تفضيلاتك الدينية.",
        "religiosity_prompt": "كيف تصف التزامك الديني؟",
        "conservative": "محافظ/تقليدي",
        "moderate": "معتدل",
        "progressive": "تقدمي/ليبرالي",
        "prayer_habits_prompt": "كم مرة تصلي؟",
        "five_times": "خمس مرات يوميًا",
        "most_prayers": "معظم الصلوات اليومية",
        "weekly": "أسبوعيًا (الجمعة)",
        "occasionally": "أحيانًا",
        "rarely": "نادرًا",
        "covering_prompt": "ما هو أسلوب الحجاب لديك؟ (للنساء)",
        "niqab": "تغطية الوجه (نقاب)",
        "hijab": "تغطية الشعر فقط (حجاب)",
        "none": "طبيعي بدون غطاء",
        "situational": "تغطية حسب المناسبة",
        "match_found": "وجدنا توافقًا محتملًا لك!",
        "compatibility_score": "نسبة التوافق: {score}%",
        "interested": "مهتم ✓",
        "not_interested": "غير مهتم ✗",
        "mutual_match": "تهانينا! لديك توافق جديد مع {name}. لقد أبديتما اهتمامًا ببعضكما البعض.",
        "group_created": "تم إنشاء مجموعة محادثة لك ولـ {name}. نتمنى أن تكون هذه بداية توافق مبارك.",
        "conversation_starters": "إليك بعض المواضيع المقترحة للمناقشة:",
        "topic_1": "قيم وتقاليد العائلة",
        "topic_2": "أهداف وطموحات الحياة",
        "topic_3": "الممارسات والمعتقدات الدينية",
        "topic_4": "توقعات الحياة الزوجية",
        "family_invitation": "هل ترغب في دعوة أحد أفراد العائلة للإشراف على هذه المحادثة؟",
        "invite_family": "دعوة فرد من العائلة",
        "later": "ربما لاحقًا",
        "personality_test_intro": "سيساعدنا تقييم الشخصية هذا في العثور على توافقات متوافقة. يرجى الإجابة بصدق.",
        "strongly_disagree": "غير موافق بشدة",
        "disagree": "غير موافق",
        "neutral": "محايد",
        "agree": "موافق",
        "strongly_agree": "موافق بشدة",
        "horoscope_intro": "اختياري: قدم معلومات ميلادك للحصول على رؤى توافق إضافية.",
        "birth_date_prompt": "ما هو تاريخ ميلادك؟",
        "birth_time_prompt": "ما هو وقت ميلادك؟ (اختياري)",
        "birth_location_prompt": "أين ولدت؟ (اختياري)",
        "skip": "تخطي هذه الخطوة",
        "profile_complete": "اكتمل ملفك الشخصي! سنبدأ في البحث عن توافقات متوافقة لك.",
        "settings_updated": "تم تحديث إعداداتك بنجاح.",
        "error_message": "حدث خطأ. يرجى المحاولة مرة أخرى لاحقًا.",
        "report_user": "الإبلاغ عن المستخدم",
        "block_user": "حظر المستخدم",
        "report_reason_prompt": "يرجى اختيار سبب للإبلاغ عن هذا المستخدم:",
        "inappropriate_behavior": "سلوك غير لائق",
        "fake_profile": "ملف شخصي مزيف",
        "harassment": "تحرش",
        "other_reason": "سبب آخر",
        "report_submitted": "تم تقديم بلاغك. شكرًا لمساعدتك في الحفاظ على سلامة مجتمعنا.",
        "blocked_user": "لقد قمت بحظر هذا المستخدم. لن يتمكن من الاتصال بك بعد الآن.",
        "success_story_prompt": "هل ترغب في مشاركة قصة نجاحك مع مجتمعنا؟",
        "share": "مشاركة قصتي",
        "keep_private": "الاحتفاظ بها خاصة",
        "thank_you": "شكرًا لاستخدام خدمتنا!"
    }
    
    # Save translation files
    with open(TRANSLATION_PATH / 'en.json', 'w', encoding='utf-8') as f:
        json.dump(en_translations, f, ensure_ascii=False, indent=2)
    
    with open(TRANSLATION_PATH / 'ar.json', 'w', encoding='utf-8') as f:
        json.dump(ar_translations, f, ensure_ascii=False, indent=2)

def get_user_language(user_id, db_session):
    """Get the user's preferred language from database."""
    from src.models import User, UserSettings
    
    user = db_session.query(User).filter(User.telegram_id == str(user_id)).first()
    if user and user.settings:
        return user.settings.language_preference
    
    return DEFAULT_LANGUAGE

def get_text(key, user_id=None, db_session=None, lang=None, **kwargs):
    """
    Get translated text for a given key.
    
    Args:
        key: The translation key
        user_id: The user's Telegram ID (to determine language preference)
        db_session: Database session
        lang: Explicitly specified language code (overrides user preference)
        **kwargs: Format parameters for the translated string
    
    Returns:
        Translated string
    """
    # Load translations if not already loaded
    if not translations:
        load_translations()
    
    # Determine language to use
    language = lang
    if not language and user_id and db_session:
        language = get_user_language(user_id, db_session)
    if not language:
        language = DEFAULT_LANGUAGE
    
    # Get translation
    if language in translations and key in translations[language]:
        text = translations[language][key]
    elif DEFAULT_LANGUAGE in translations and key in translations[DEFAULT_LANGUAGE]:
        text = translations[DEFAULT_LANGUAGE][key]
    else:
        text = key
    
    # Apply format parameters if provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception as e:
            print(f"Error formatting translation for key {key}: {e}")
    
    return text

def get_all_translations(key):
    """Get all available translations for a key."""
    result = {}
    for lang, trans in translations.items():
        if key in trans:
            result[lang] = trans[key]
    return result

# Initialize translations on module import
load_translations()
