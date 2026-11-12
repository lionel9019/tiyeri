from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class ChatbotIntent(Base):
    __tablename__ = "chatbot_intentions"
    id = Column(Integer, primary_key=True, index=True)
    intent_name = Column(String(100), unique=True, index=True)
    keywords = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
