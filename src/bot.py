"""
Main bot implementation for the Traditional Matchmaking Telegram Bot.
"""

import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)
from sqlalchemy.orm import Session

from src.config import BOT_TOKEN, DEFAULT_LANGUAGE
from src.database import init_db, get_session
from src.models import (
    User, Profile, Match, Conversation, Message, UserSettings,
    Gender, ReligiosityLevel, CoveringStyle, MatchStatus
)
from src.translations import get_text, load_translations
from src.matching import (
    calculate_overall_compatibility, score_personality_test,
    determine_zodiac_sign
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    LANGUAGE_SELECTION, TERMS_ACCEPTANCE, AGE_VERIFICATION,
    BASIC_INFO, RELIGIOUS_INFO, PERSONALITY_TEST, HOROSCOPE_INFO,
    MATCHING, CONVERSATION, SETTINGS
) = range(10)

# Basic info sub-states
(
    NAME, AGE, GENDER, NATIONALITY, CITY, EDUCATION, PROFESSION
) = range(7)

# Religious info sub-states
(
    RELIGIOSITY, PRAYER_HABITS, COVERING_STYLE
) = range(3)

# Personality test state
PERSONALITY_QUESTION = 0

# Horoscope info sub-states
(
    BIRTH_DATE, BIRTH_TIME, BIRTH_LOCATION
) = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask for language preference."""
    user = update.effective_user
    
    # Initialize user data
    context.user_data.clear()
    
    # Check if user exists in database
    session = get_session()
    db_user = session.query(User).filter(User.telegram_id == str(user.id)).first()
    
    if db_user:
        # User exists, load their language preference
        if db_user.settings:
            context.user_data['language'] = db_user.settings.language_preference
        else:
            context.user_data['language'] = DEFAULT_LANGUAGE
        
        # Check if user has completed profile
        if db_user.profile:
            # User has a profile, go to main menu
            await send_main_menu(update, context)
            session.close()
            return MATCHING
    else:
        # New user, create record
        new_user = User(
            telegram_id=str(user.id),
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code or DEFAULT_LANGUAGE
        )
        session.add(new_user)
        session.commit()
        
        # Set default language
        context.user_data['language'] = user.language_code or DEFAULT_LANGUAGE
    
    session.close()
    
    # Ask for language preference
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("العربية", callback_data="lang_ar")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the Traditional Matchmaking Bot for Saudi Arabia and GCC nationals.\n\n"
        "مرحبًا بك في روبوت التوفيق التقليدي للسعوديين ومواطني دول مجلس التعاون الخليجي.\n\n"
        "Please select your preferred language / يرجى اختيار لغتك المفضلة:",
        reply_markup=reply_markup
    )
    
    return LANGUAGE_SELECTION

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle language selection."""
    query = update.callback_query
    await query.answer()
    
    # Get selected language
    language = query.data.split('_')[1]
    context.user_data['language'] = language
    
    # Update user's language preference in database
    session = get_session()
    user = session.query(User).filter(User.telegram_id == str(query.from_user.id)).first()
    
    if user:
        if not user.settings:
            # Create settings if they don't exist
            settings = UserSettings(user_id=user.id, language_preference=language)
            session.add(settings)
        else:
            # Update existing settings
            user.settings.language_preference = language
        
        session.commit()
    
    session.close()
    
    # Show terms and conditions
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("accept", lang=language),
                callback_data="terms_accept"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("decline", lang=language),
                callback_data="terms_decline"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text("terms_acceptance", lang=language) + "\n\n" +
        "Terms and Conditions: [Link to Terms]\n" +
        "Privacy Policy: [Link to Privacy Policy]",
        reply_markup=reply_markup
    )
    
    return TERMS_ACCEPTANCE

async def terms_acceptance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle terms and conditions acceptance."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    if query.data == "terms_decline":
        await query.edit_message_text(
            get_text("thank_you", lang=language) + "\n\n" +
            "You must accept the Terms and Conditions to use this service. "
            "Type /start to try again."
        )
        return ConversationHandler.END
    
    # Terms accepted, verify age
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("yes", lang=language),
                callback_data="age_yes"
            ),
            InlineKeyboardButton(
                get_text("no", lang=language),
                callback_data="age_no"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text("age_verification", lang=language),
        reply_markup=reply_markup
    )
    
    return AGE_VERIFICATION

async def age_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle age verification."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    if query.data == "age_no":
        await query.edit_message_text(
            get_text("under_18_message", lang=language)
        )
        return ConversationHandler.END
    
    # Age verified, start profile setup
    await query.edit_message_text(
        get_text("basic_info_prompt", lang=language)
    )
    
    # Ask for name
    await query.message.reply_text(
        get_text("name_prompt", lang=language)
    )
    
    return BASIC_INFO

async def basic_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle basic information collection."""
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    # Determine which basic info field we're collecting
    if 'basic_info_state' not in context.user_data:
        context.user_data['basic_info_state'] = NAME
    
    current_state = context.user_data['basic_info_state']
    
    if current_state == NAME:
        # Save name
        context.user_data['name'] = update.message.text
        
        # Check if user has a profile photo
        user = update.effective_user
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        
        if photos.total_count == 0:
            # User doesn't have a profile photo, request one
            await update.message.reply_text(
                "A profile photo is mandatory. Please set a profile photo in your Telegram settings and then continue.\n\n"
                "في التلغرام الخاص بك وثم استمر. الصورة الشخصية إلزامية. يرجى تعيين صورة شخصية"
            )
            return BASIC_INFO
        
        # Ask for age
        await update.message.reply_text(
            get_text("age_prompt", lang=language)
        )
        context.user_data['basic_info_state'] = AGE
        return BASIC_INFO
    
    elif current_state == AGE:
        # Validate and save age
        try:
            age = int(update.message.text)
            if age < 18 or age > 100:
                await update.message.reply_text(
                    "Please enter a valid age between 18 and 100."
                )
                return BASIC_INFO
            
            context.user_data['age'] = age
            
            # Ask for gender
            keyboard = [
                [
                    InlineKeyboardButton(
                        get_text("male", lang=language),
                        callback_data="gender_male"
                    ),
                    InlineKeyboardButton(
                        get_text("female", lang=language),
                        callback_data="gender_female"
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                get_text("gender_prompt", lang=language),
                reply_markup=reply_markup
            )
            
            context.user_data['basic_info_state'] = GENDER
            return BASIC_INFO
            
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid number for your age."
            )
            return BASIC_INFO
    
    # Other basic info states would be handled here
    
    # After collecting all basic info, move to religious info
    return RELIGIOUS_INFO

async def gender_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle gender selection."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    # Save gender
    gender = query.data.split('_')[1]
    context.user_data['gender'] = gender
    
    # Ask for nationality
    await query.edit_message_text(
        get_text("nationality_prompt", lang=language)
    )
    
    context.user_data['basic_info_state'] = NATIONALITY
    return BASIC_INFO

async def save_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save user profile to database."""
    user_id = update.effective_user.id
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    session = get_session()
    user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    
    if not user:
        # This shouldn't happen, but just in case
        await update.message.reply_text(
            "An error occurred. Please restart with /start"
        )
        session.close()
        return ConversationHandler.END
    
    # Check if user already has a profile
    if not user.profile:
        # Create new profile
        profile = Profile(
            user_id=user.id,
            age=context.user_data.get('age'),
            gender=Gender.MALE if context.user_data.get('gender') == 'male' else Gender.FEMALE,
            nationality=context.user_data.get('nationality'),
            city=context.user_data.get('city'),
            education_level=context.user_data.get('education'),
            profession=context.user_data.get('profession'),
            religiosity_level=ReligiosityLevel(context.user_data.get('religiosity', 'moderate')),
            prayer_habits=context.user_data.get('prayer_habits'),
            personal_covering=CoveringStyle(context.user_data.get('covering', 'none')) if context.user_data.get('gender') == 'female' else None,
            personality_type=context.user_data.get('personality_type'),
            personality_details=context.user_data.get('personality_details'),
            birth_date=context.user_data.get('birth_date'),
            birth_time=context.user_data.get('birth_time'),
            birth_location=context.user_data.get('birth_location'),
            zodiac_sign=context.user_data.get('zodiac_sign')
        )
        session.add(profile)
    else:
        # Update existing profile
        profile = user.profile
        profile.age = context.user_data.get('age', profile.age)
        profile.gender = Gender.MALE if context.user_data.get('gender') == 'male' else Gender.FEMALE
        profile.nationality = context.user_data.get('nationality', profile.nationality)
        profile.city = context.user_data.get('city', profile.city)
        profile.education_level = context.user_data.get('education', profile.education_level)
        profile.profession = context.user_data.get('profession', profile.profession)
        
        if 'religiosity' in context.user_data:
            profile.religiosity_level = ReligiosityLevel(context.user_data.get('religiosity'))
        
        profile.prayer_habits = context.user_data.get('prayer_habits', profile.prayer_habits)
        
        if context.user_data.get('gender') == 'female' and 'covering' in context.user_data:
            profile.personal_covering = CoveringStyle(context.user_data.get('covering'))
        
        if 'personality_type' in context.user_data:
            profile.personality_type = context.user_data.get('personality_type')
            profile.personality_details = context.user_data.get('personality_details')
        
        if 'birth_date' in context.user_data:
            profile.birth_date = context.user_data.get('birth_date')
            profile.birth_time = context.user_data.get('birth_time')
            profile.birth_location = context.user_data.get('birth_location')
            profile.zodiac_sign = context.user_data.get('zodiac_sign')
    
    session.commit()
    session.close()
    
    # Clear user data
    context.user_data.clear()
    context.user_data['language'] = language
    
    # Send confirmation and go to main menu
    await update.message.reply_text(
        get_text("profile_complete", lang=language)
    )
    
    await send_main_menu(update, context)
    return MATCHING

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the main menu."""
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("view_matches", lang=language),
                callback_data="menu_matches"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("conversations", lang=language),
                callback_data="menu_conversations"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("profile_setup", lang=language),
                callback_data="menu_profile"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("family_involvement", lang=language),
                callback_data="menu_family"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("settings", lang=language),
                callback_data="menu_settings"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("help", lang=language),
                callback_data="menu_help"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            get_text("main_menu", lang=language),
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            get_text("main_menu", lang=language),
            reply_markup=reply_markup
        )

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main menu selections."""
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    selection = query.data.split('_')[1]
    
    if selection == "matches":
        # Show potential matches
        await show_potential_matches(update, context)
        return MATCHING
    
    elif selection == "conversations":
        # Show active conversations
        await show_conversations(update, context)
        return CONVERSATION
    
    elif selection == "profile":
        # Go to profile setup
        await query.edit_message_text(
            get_text("basic_info_prompt", lang=language)
        )
        return BASIC_INFO
    
    elif selection == "family":
        # Family involvement features
        await query.edit_message_text(
            get_text("family_invitation", lang=language)
        )
        return MATCHING
    
    elif selection == "settings":
        # Settings menu
        await show_settings(update, context)
        return SETTINGS
    
    elif selection == "help":
        # Help information
        await query.edit_message_text(
            "Help and support information will be displayed here.\n\n"
            "To return to the main menu, use /start"
        )
        return MATCHING
    
    return MATCHING

async def show_potential_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show potential matches to the user."""
    query = update.callback_query
    user_id = query.from_user.id
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    session = get_session()
    user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    
    if not user or not user.profile:
        await query.edit_message_text(
            "Please complete your profile first."
        )
        session.close()
        return
    
    # Find potential matches
    # This is a simplified version - in a real implementation, you would:
    # 1. Filter by gender preference
    # 2. Filter by age range
    # 3. Filter by other criteria
    # 4. Calculate compatibility scores
    # 5. Sort by compatibility
    
    # For demo purposes, just get users of opposite gender
    opposite_gender = Gender.FEMALE if user.profile.gender == Gender.MALE else Gender.MALE
    
    potential_matches = session.query(User).join(Profile).filter(
        Profile.gender == opposite_gender,
        User.id != user.id
    ).limit(5).all()
    
    if not potential_matches:
        await query.edit_message_text(
            get_text("No potential matches found at this time. Please check back later.", lang=language) +
            "\n\n" + get_text("Return to main menu with /start", lang=language)
        )
        session.close()
        return
    
    # Show the first potential match
    match_index = context.user_data.get('match_index', 0)
    if match_index >= len(potential_matches):
        match_index = 0
    
    current_match = potential_matches[match_index]
    
    # Calculate compatibility score
    compatibility_score = calculate_overall_compatibility(user.profile, current_match.profile)
    
    # Create match display
    match_text = (
        f"{get_text('match_found', lang=language)}\n\n"
        f"Name: {current_match.first_name}\n"
        f"Age: {current_match.profile.age}\n"
        f"Nationality: {current_match.profile.nationality}\n"
        f"City: {current_match.profile.city}\n"
        f"Education: {current_match.profile.education_level}\n"
        f"Profession: {current_match.profile.profession}\n\n"
        f"{get_text('compatibility_score', lang=language, score=int(compatibility_score))}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("interested", lang=language),
                callback_data=f"match_yes_{current_match.id}"
            ),
            InlineKeyboardButton(
                get_text("not_interested", lang=language),
                callback_data=f"match_no_{current_match.id}"
            )
        ],
        [
            InlineKeyboardButton(
                "Return to Main Menu",
                callback_data="return_main"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        match_text,
        reply_markup=reply_markup
    )
    
    # Update match index for next time
    context.user_data['match_index'] = match_index + 1
    
    session.close()

async def match_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user response to a potential match."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    response, match_id = query.data.split('_')[1:3]
    match_id = int(match_id)
    
    session = get_session()
    user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    
    if not user:
        await query.edit_message_text(
            "An error occurred. Please restart with /start"
        )
        session.close()
        return MATCHING
    
    if response == "yes":
        # User is interested in the match
        # Check if there's already a match in the opposite direction
        existing_match = session.query(Match).filter(
            Match.sender_id == match_id,
            Match.receiver_id == user.id,
            Match.status == MatchStatus.PENDING
        ).first()
        
        if existing_match:
            # Mutual match! Update status and create conversation
            existing_match.status = MatchStatus.ACCEPTED
            
            # Create a new conversation
            conversation = Conversation(match_id=existing_match.id)
            conversation.participants.append(user)
            conversation.participants.append(existing_match.sender)
            
            session.add(conversation)
            session.commit()
            
            # Notify the other user (in a real bot, you would send them a message)
            
            # Notify current user
            match_user = session.query(User).filter(User.id == match_id).first()
            
            await query.edit_message_text(
                get_text("mutual_match", lang=language, name=match_user.first_name) + "\n\n" +
                get_text("group_created", lang=language, name=match_user.first_name) + "\n\n" +
                get_text("conversation_starters", lang=language) + "\n" +
                "1. " + get_text("topic_1", lang=language) + "\n" +
                "2. " + get_text("topic_2", lang=language) + "\n" +
                "3. " + get_text("topic_3", lang=language) + "\n" +
                "4. " + get_text("topic_4", lang=language)
            )
            
            session.close()
            return CONVERSATION
        else:
            # Create a new match
            new_match = Match(
                sender_id=user.id,
                receiver_id=match_id,
                status=MatchStatus.PENDING,
                compatibility_score=75  # This would be calculated properly in a real implementation
            )
            
            session.add(new_match)
            session.commit()
            
            # Show next match
            await show_potential_matches(update, context)
    else:
        # User is not interested
        # In a real implementation, you might want to record this to avoid showing the same match again
        
        # Show next match
        await show_potential_matches(update, context)
    
    session.close()
    return MATCHING

async def show_conversations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's active conversations."""
    query = update.callback_query
    user_id = query.from_user.id
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    session = get_session()
    user = session.query(User).filter(User.telegram_id == str(user_id)).first()
    
    if not user:
        await query.edit_message_text(
            "An error occurred. Please restart with /start"
        )
        session.close()
        return
    
    # Get user's conversations
    conversations = user.conversations
    
    if not conversations:
        await query.edit_message_text(
            "You don't have any active conversations yet.\n\n"
            "Return to main menu with /start"
        )
        session.close()
        return
    
    # Create list of conversations
    keyboard = []
    
    for conversation in conversations:
        # Find the other participant
        other_participant = next((p for p in conversation.participants if p.id != user.id), None)
        
        if other_participant:
            keyboard.append([
                InlineKeyboardButton(
                    f"Chat with {other_participant.first_name}",
                    callback_data=f"conv_{conversation.id}"
                )
            ])
    
    keyboard.append([
        InlineKeyboardButton(
            "Return to Main Menu",
            callback_data="return_main"
        )
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text("conversations", lang=language),
        reply_markup=reply_markup
    )
    
    session.close()

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu."""
    query = update.callback_query
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    
    keyboard = [
        [
            InlineKeyboardButton(
                "Change Language",
                callback_data="settings_language"
            )
        ],
        [
            InlineKeyboardButton(
                "Privacy Settings",
                callback_data="settings_privacy"
            )
        ],
        [
            InlineKeyboardButton(
                "Matching Preferences",
                callback_data="settings_matching"
            )
        ],
        [
            InlineKeyboardButton(
                "Return to Main Menu",
                callback_data="return_main"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text("settings", lang=language),
        reply_markup=reply_markup
    )

async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to main menu."""
    query = update.callback_query
    await query.answer()
    
    await send_main_menu(update, context)
    return MATCHING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    
    await update.message.reply_text(
        "Conversation ended. Type /start to begin again."
    )
    
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Initialize database
    init_db()
    
    # Load translations
    load_translations()
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE_SELECTION: [
                CallbackQueryHandler(language_selection, pattern=r"^lang_")
            ],
            TERMS_ACCEPTANCE: [
                CallbackQueryHandler(terms_acceptance, pattern=r"^terms_")
            ],
            AGE_VERIFICATION: [
                CallbackQueryHandler(age_verification, pattern=r"^age_")
            ],
            BASIC_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, basic_info),
                CallbackQueryHandler(gender_selection, pattern=r"^gender_")
            ],
            RELIGIOUS_INFO: [
                # Handlers for religious info would go here
            ],
            PERSONALITY_TEST: [
                # Handlers for personality test would go here
            ],
            HOROSCOPE_INFO: [
                # Handlers for horoscope info would go here
            ],
            MATCHING: [
                CallbackQueryHandler(main_menu_handler, pattern=r"^menu_"),
                CallbackQueryHandler(match_response, pattern=r"^match_"),
                CallbackQueryHandler(return_to_main_menu, pattern=r"^return_main$")
            ],
            CONVERSATION: [
                # Handlers for conversation would go here
                CallbackQueryHandler(return_to_main_menu, pattern=r"^return_main$")
            ],
            SETTINGS: [
                # Handlers for settings would go here
                CallbackQueryHandler(return_to_main_menu, pattern=r"^return_main$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(conv_handler)
    
    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()
