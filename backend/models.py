from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from backend.database.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    chatbot_resources = relationship("ChatbotResource", back_populates="owner")


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)


class Culture(Base):
    __tablename__ = "cultures"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)


class CalendrierCulture(Base):
    __tablename__ = "calendrier_cultures"
    id = Column(Integer, primary_key=True, index=True)
    culture_id = Column(Integer, ForeignKey("cultures.id"))
    saison = Column(String(255))
    details = Column(Text)

    culture = relationship("Culture")


class Diagnostic(Base):
    __tablename__ = "diagnostics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resultat = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    images = relationship("AnalyseImage", back_populates="diagnostic")


class DiagnosticResponse(Base):
    __tablename__ = "diagnostic_reponses"
    id = Column(Integer, primary_key=True, index=True)
    nom_diagnostic = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    traitement = Column(Text)
    conseils = Column(Text)
    culture = Column(String(255))
    nom_scientifique = Column(String(255))
    origine = Column(String(255))
    sol = Column(String(255))
    varietes = Column(Text)
    rendement = Column(Text)
    nutrition = Column(Text)
    toxicite = Column(Text)
    medicinal = Column(Text)
    produits = Column(Text)
    saisons = Column(Text)
    itineraire = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AnalyseImage(Base):
    __tablename__ = "analyses_images"
    id = Column(Integer, primary_key=True, index=True)
    diagnostic_id = Column(Integer, ForeignKey("diagnostics.id"))
    image_path = Column(String(255))
    resultat = Column(Text)

    diagnostic = relationship("Diagnostic", back_populates="images")


class ConsultationImage(Base):
    __tablename__ = "consultation_images"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String(255))
    commentaire = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan")


class Symptom(Base):
    __tablename__ = "symptomes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)


class ChatbotIntent(Base):
    __tablename__ = "chatbot_intents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    response = Column(Text)


class ChatbotLearning(Base):
    __tablename__ = "chatbot_learnings"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(Text)
    intent_id = Column(Integer, ForeignKey("chatbot_intents.id"))

    intent = relationship("ChatbotIntent")


class ChatbotResource(Base):
    __tablename__ = "chatbot_resources"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(255))
    content = Column(Text)

    owner = relationship("User", back_populates="chatbot_resources")


class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255))
    contenu = Column(Text)


class LearnedPhrase(Base):
    __tablename__ = "learned_phrases"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(Text)
    intent = Column(String(255))


class QueryLog(Base):
    __tablename__ = "query_logs"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Administration(Base):
    __tablename__ = "administrations"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)


class AgriculturalResource(Base):
    __tablename__ = "agricultural_resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
