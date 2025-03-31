# Arabic Translation Implementation

This document outlines the approach for implementing full Arabic translation support in the semi-dating Telegram bot for Saudi Arabia and GCC nationals.

## Translation Strategy

### Bilingual Interface
- Complete dual-language support (Arabic and English)
- Language toggle in settings menu
- Default language detection based on user's Telegram language setting
- Option to view specific content in alternate language

### Translation Quality Assurance
- Professional translation by native Gulf Arabic speakers
- Cultural context adaptation, not just literal translation
- Religious terminology review by qualified individuals
- Dialect considerations for Gulf Arabic region

## Content for Translation

### User Interface Elements
```json
{
  "welcome_message": {
    "en": "Welcome to the Traditional Matchmaking Bot for Saudi Arabia and GCC nationals. This service is designed to help you find a suitable marriage partner while respecting cultural and religious values.",
    "ar": "مرحبًا بك في روبوت التوفيق التقليدي للسعوديين ومواطني دول مجلس التعاون الخليجي. تم تصميم هذه الخدمة لمساعدتك في العثور على شريك زواج مناسب مع احترام القيم الثقافية والدينية."
  },
  "main_menu": {
    "en": "Main Menu",
    "ar": "القائمة الرئيسية"
  },
  "profile_setup": {
    "en": "Profile Setup",
    "ar": "إعداد الملف الشخصي"
  },
  "view_matches": {
    "en": "View Potential Matches",
    "ar": "عرض التوافقات المحتملة"
  },
  "settings": {
    "en": "Settings",
    "ar": "الإعدادات"
  },
  "family_involvement": {
    "en": "Family Involvement",
    "ar": "مشاركة العائلة"
  },
  "conversations": {
    "en": "My Conversations",
    "ar": "محادثاتي"
  },
  "help": {
    "en": "Help & Support",
    "ar": "المساعدة والدعم"
  }
}
```

### Profile Questions
```json
{
  "basic_info": {
    "name": {
      "en": "What is your name? (First name or partial name for privacy)",
      "ar": "ما هو اسمك؟ (الاسم الأول أو جزء من الاسم للخصوصية)"
    },
    "age": {
      "en": "What is your age?",
      "ar": "كم عمرك؟"
    },
    "gender": {
      "en": "What is your gender?",
      "ar": "ما هو جنسك؟"
    },
    "nationality": {
      "en": "What is your nationality?",
      "ar": "ما هي جنسيتك؟"
    },
    "city": {
      "en": "In which city do you live?",
      "ar": "في أي مدينة تعيش؟"
    },
    "education": {
      "en": "What is your highest level of education?",
      "ar": "ما هو أعلى مستوى تعليمي لديك؟"
    },
    "profession": {
      "en": "What is your profession?",
      "ar": "ما هي مهنتك؟"
    }
  },
  "religious_info": {
    "religiosity_level": {
      "en": "How would you describe your religious observance?",
      "ar": "كيف تصف التزامك الديني؟"
    },
    "options": {
      "conservative": {
        "en": "Conservative/Traditional",
        "ar": "محافظ/تقليدي"
      },
      "moderate": {
        "en": "Moderate",
        "ar": "معتدل"
      },
      "progressive": {
        "en": "Progressive/Liberal",
        "ar": "تقدمي/ليبرالي"
      }
    }
  },
  "covering_preferences": {
    "personal_covering": {
      "en": "What is your covering style? (For women)",
      "ar": "ما هو أسلوب الحجاب لديك؟ (للنساء)"
    },
    "options": {
      "niqab": {
        "en": "Face covering (niqab)",
        "ar": "تغطية الوجه (نقاب)"
      },
      "hijab": {
        "en": "Hair covering only (hijab)",
        "ar": "تغطية الشعر فقط (حجاب)"
      },
      "none": {
        "en": "Natural with no covers",
        "ar": "طبيعي بدون غطاء"
      },
      "situational": {
        "en": "Situational covering",
        "ar": "تغطية حسب المناسبة"
      }
    }
  }
}
```

### Personality Test
```json
{
  "intro": {
    "en": "This personality assessment will help us find compatible matches. Please answer honestly.",
    "ar": "سيساعدنا تقييم الشخصية هذا في العثور على توافقات متوافقة. يرجى الإجابة بصدق."
  },
  "questions": {
    "q1": {
      "en": "You prefer spending time with a small group of close friends rather than at large social gatherings.",
      "ar": "تفضل قضاء الوقت مع مجموعة صغيرة من الأصدقاء المقربين بدلاً من التجمعات الاجتماعية الكبيرة."
    },
    "q2": {
      "en": "You often focus more on details than the big picture.",
      "ar": "غالبًا ما تركز على التفاصيل أكثر من الصورة الكبيرة."
    }
  },
  "results": {
    "INTJ": {
      "en": "Architect: Strategic, innovative thinker with a plan for everything",
      "ar": "المهندس: مفكر استراتيجي مبتكر لديه خطة لكل شيء"
    },
    "ENFP": {
      "en": "Campaigner: Enthusiastic, creative, sociable free spirit who finds potential in every opportunity",
      "ar": "المناصر: روح حرة متحمسة ومبدعة واجتماعية تجد إمكانات في كل فرصة"
    }
  }
}
```

### System Messages
```json
{
  "match_notification": {
    "en": "Congratulations! You have a new match with {name}. You both expressed interest in each other.",
    "ar": "تهانينا! لديك توافق جديد مع {name}. لقد أبديتما اهتمامًا ببعضكما البعض."
  },
  "group_creation": {
    "en": "A conversation group has been created for you and {name}. May this be the beginning of a blessed connection.",
    "ar": "تم إنشاء مجموعة محادثة لك ولـ {name}. نتمنى أن تكون هذه بداية توافق مبارك."
  },
  "family_invitation": {
    "en": "You have invited {family_member} to oversee your conversation with {match_name}.",
    "ar": "لقد دعوت {family_member} للإشراف على محادثتك مع {match_name}."
  },
  "rejection": {
    "en": "You have passed on this match. They will not be shown to you again.",
    "ar": "لقد تجاوزت هذا التوافق. لن يتم عرضه عليك مرة أخرى."
  }
}
```

## Technical Implementation

### Translation Storage
- JSON format for all translatable content
- Database structure with language code fields
- Content management system for easy updates

### Language Detection and Selection
```python
def get_user_language(user_id):
    # Check user preference in database
    user_pref = db.get_user_language_preference(user_id)
    if user_pref:
        return user_pref
    
    # Fall back to Telegram language setting
    telegram_lang = get_telegram_language(user_id)
    if telegram_lang in ['ar', 'ar-SA']:
        return 'ar'
    
    # Default to English
    return 'en'

def get_text(key, user_id):
    lang = get_user_language(user_id)
    
    # Get text from translations database
    text = translations.get(key, lang)
    
    # Fall back to English if translation missing
    if not text and lang != 'en':
        text = translations.get(key, 'en')
    
    # Fall back to key if no translation found
    return text or key
```

### Right-to-Left (RTL) Support
- Proper RTL text rendering in all interfaces
- Bidirectional text handling
- RTL-aware UI layouts and button positioning
- Direction-sensitive keyboard layouts

### Number and Date Formatting
- Arabic numeral options (١٢٣ vs 123)
- Hijri calendar integration for dates
- Localized time formats
- Regional date notation

## Cultural Adaptation

### Dialectal Considerations
- Focus on Gulf Arabic dialect
- Common expressions and idioms from the region
- Formal vs. informal language options
- Age-appropriate language

### Religious Terminology
- Accurate translation of Islamic concepts
- Appropriate honorifics (SAW, RA, etc.)
- Consistent use of religious terms
- Respectful language for religious concepts

### Cultural References
- Region-specific examples and metaphors
- Culturally relevant success stories
- Local customs and traditions references
- GCC-specific social norms

## Implementation Process

### Translation Workflow
1. Extract all translatable content
2. Professional translation by native speakers
3. Cultural review by Saudi/GCC experts
4. Religious terminology review
5. Technical implementation
6. Quality assurance testing
7. User feedback collection
8. Continuous improvement

### Quality Assurance
- Native speaker review
- Context verification
- Functional testing in both languages
- User experience testing with Arabic speakers
- Feedback mechanism for translation improvements

## Maintenance Plan

### Content Updates
- Translation update process for new features
- Version control for translations
- Change tracking for modified content
- Translation memory for consistency

### User Feedback Integration
- Reporting mechanism for translation issues
- Community input for dialectal improvements
- Regular review and update cycles
- A/B testing for alternative translations

## Accessibility Considerations

### Text Size and Readability
- Font selection optimized for Arabic script
- Adjustable text size options
- High contrast mode
- Screen reader compatibility

### Voice and Audio
- Text-to-speech support for both languages
- Voice input options
- Audio pronunciation guides for key terms
- Multilingual voice commands
