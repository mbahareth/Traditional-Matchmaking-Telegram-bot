"""
Database models for the Traditional Matchmaking Telegram Bot.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, 
    DateTime, ForeignKey, Table, Text, JSON, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

# Association tables for many-to-many relationships
user_interests = Table(
    'user_interests', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('interest_id', Integer, ForeignKey('interests.id'))
)

user_family_members = Table(
    'user_family_members', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('family_member_id', Integer, ForeignKey('family_members.id'))
)

# Enum definitions
class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class ReligiosityLevel(enum.Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    PROGRESSIVE = "progressive"

class CoveringStyle(enum.Enum):
    NIQAB = "niqab"
    HIJAB = "hijab"
    NONE = "none"
    SITUATIONAL = "situational"

class MatchStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class AccountStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    BANNED = "banned"

class VerificationLevel(enum.Enum):
    NONE = "none"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    FULL = "full"

# Main models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False)
    language_code = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    sent_matches = relationship("Match", foreign_keys="Match.sender_id", back_populates="sender")
    received_matches = relationship("Match", foreign_keys="Match.receiver_id", back_populates="receiver")
    conversations = relationship("Conversation", secondary="conversation_participants", back_populates="participants")
    reports_filed = relationship("Report", foreign_keys="Report.reporter_id", back_populates="reporter")
    reports_received = relationship("Report", foreign_keys="Report.reported_id", back_populates="reported")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, first_name={self.first_name})>"

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    # Basic Information
    age = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    nationality = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    education_level = Column(String(100), nullable=True)
    profession = Column(String(100), nullable=True)
    family_background = Column(String(255), nullable=True)
    
    # Religious Information
    religiosity_level = Column(Enum(ReligiosityLevel), nullable=True)
    prayer_habits = Column(String(100), nullable=True)
    religious_education = Column(String(100), nullable=True)
    religious_practices = Column(JSON, nullable=True)  # Array of strings
    
    # Marriage Preferences
    marriage_timeline = Column(String(100), nullable=True)
    living_arrangement = Column(String(100), nullable=True)
    role_expectations = Column(JSON, nullable=True)  # Object with husband_role and wife_role
    family_size = Column(String(100), nullable=True)
    
    # Personal Interests (many-to-many)
    interests = relationship("Interest", secondary=user_interests, back_populates="users")
    
    # Covering Preferences (for women)
    personal_covering = Column(Enum(CoveringStyle), nullable=True)
    partner_covering_preference = Column(Enum(CoveringStyle), nullable=True)
    covering_importance = Column(Integer, nullable=True)  # 1-5 scale
    
    # Personality Assessment
    personality_type = Column(String(4), nullable=True)  # MBTI type (e.g., INTJ)
    personality_details = Column(JSON, nullable=True)  # Detailed scores
    
    # Horoscope Information
    birth_date = Column(DateTime, nullable=True)
    birth_time = Column(String(10), nullable=True)
    birth_location = Column(String(100), nullable=True)
    zodiac_sign = Column(String(20), nullable=True)
    
    # Verification
    verified = Column(Boolean, default=False)
    verification_level = Column(Enum(VerificationLevel), default=VerificationLevel.NONE)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(id={self.id}, user_id={self.user_id}, age={self.age}, gender={self.gender})>"

class Interest(Base):
    __tablename__ = 'interests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=True)
    
    # Relationships
    users = relationship("Profile", secondary=user_interests, back_populates="interests")
    
    def __repr__(self):
        return f"<Interest(id={self.id}, name={self.name}, category={self.category})>"

class FamilyMember(Base):
    __tablename__ = 'family_members'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), nullable=True)
    relation = Column(String(50), nullable=False)  # Father, Mother, Brother, etc.
    name = Column(String(100), nullable=False)
    access_level = Column(String(50), nullable=False)  # Full, Limited, View-only
    
    # Relationships
    users = relationship("User", secondary=user_family_members)
    conversations = relationship("Conversation", secondary="family_conversation_access")
    
    def __repr__(self):
        return f"<FamilyMember(id={self.id}, relation={self.relation}, name={self.name})>"

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    compatibility_score = Column(Float, nullable=False)
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_matches")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_matches")
    conversation = relationship("Conversation", back_populates="match", uselist=False)
    
    def __repr__(self):
        return f"<Match(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, status={self.status})>"

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=True)
    group_chat_id = Column(String(50), nullable=True)
    stage = Column(Integer, default=1)  # Progressive stages of conversation
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.datetime.utcnow)
    is_family_supervised = Column(Boolean, default=False)
    
    # Relationships
    match = relationship("Match", back_populates="conversation")
    participants = relationship("User", secondary="conversation_participants", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    family_supervisors = relationship("FamilyMember", secondary="family_conversation_access")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, match_id={self.match_id}, stage={self.stage})>"

# Association table for conversation participants
conversation_participants = Table(
    'conversation_participants', Base.metadata,
    Column('conversation_id', Integer, ForeignKey('conversations.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

# Association table for family conversation access
family_conversation_access = Table(
    'family_conversation_access', Base.metadata,
    Column('conversation_id', Integer, ForeignKey('conversations.id')),
    Column('family_member_id', Integer, ForeignKey('family_members.id'))
)

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_template = Column(Boolean, default=False)
    template_id = Column(String(50), nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender_id={self.sender_id})>"

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    reporter_id = Column(Integer, ForeignKey('users.id'))
    reported_id = Column(Integer, ForeignKey('users.id'))
    reason = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, reviewed, resolved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reports_filed")
    reported = relationship("User", foreign_keys=[reported_id], back_populates="reports_received")
    
    def __repr__(self):
        return f"<Report(id={self.id}, reporter_id={self.reporter_id}, reported_id={self.reported_id}, status={self.status})>"

class SuccessStory(Base):
    __tablename__ = 'success_stories'
    
    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey('users.id'))
    user2_id = Column(Integer, ForeignKey('users.id'))
    outcome = Column(String(50), nullable=False)  # Meeting, Engagement, Marriage
    date = Column(DateTime, nullable=False)
    testimonial = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<SuccessStory(id={self.id}, user1_id={self.user1_id}, user2_id={self.user2_id}, outcome={self.outcome})>"

class UserSettings(Base):
    __tablename__ = 'user_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    # Privacy Settings
    profile_visibility = Column(String(50), default="all")  # all, matched, approved
    photo_visibility = Column(String(50), default="all")  # Photos are always visible to all users
    
    # Matching Preferences
    age_range_min = Column(Integer, nullable=True)
    age_range_max = Column(Integer, nullable=True)
    preferred_nationalities = Column(JSON, nullable=True)  # Array of strings
    preferred_education = Column(JSON, nullable=True)  # Array of strings
    preferred_professions = Column(JSON, nullable=True)  # Array of strings
    distance_preference = Column(Integer, nullable=True)  # Maximum distance in km
    
    # Importance Weights
    religious_compatibility_importance = Column(Integer, default=5)  # 1-5 scale
    family_background_importance = Column(Integer, default=3)  # 1-5 scale
    
    # Feature Toggles
    enable_personality_matching = Column(Boolean, default=True)
    enable_horoscope = Column(Boolean, default=True)
    
    # Communication Preferences
    initial_contact_method = Column(String(50), default="structured")  # structured, family-supervised, direct
    language_preference = Column(String(10), default="en")  # en, ar
    
    # Family Involvement
    family_approval_required = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="settings")
    
    def __repr__(self):
        return f"<UserSettings(id={self.id}, user_id={self.user_id})>"
