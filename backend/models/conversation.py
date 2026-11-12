from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from backend.database.base import Base  # ✅ import correct


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
     # Relation avec l’utilisateur
    user = relationship("User", back_populates="conversations")

    # Relation avec les messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", lazy="selectin")


    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(String(50), nullable=False)  # "user" ou "bot"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    intention = Column(String(255), nullable=True)
    conversation = relationship("Conversation", back_populates="messages")
