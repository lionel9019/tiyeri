from backend.database.base import Base

# Importer explicitement tous les modèles pour qu’Alembic les détecte

# Entités de base
from .user import User
from .zone import Zone
from .culture import Culture
from .calendrier_culture import CalendrierCulture

# Diagnostics
from .diagnostic import Diagnostic
from .diagnostic_response import DiagnosticResponse
#from .analyse_image import AnalyseImage
#from .consultation_image import ConsultationImage
#from .symptome import Symptome

# Conversation et chatbot
from .conversation import Conversation, Message
from .chatbot_intent import ChatbotIntent
#from .chatbot_learning import ChatbotLearning
#from .chatbot_intent import ChatbotResource
from .learned_phrase import LearnedPhrase
#from .knowledge import Knowledge
#from .query_log import QueryLog

# Business / administration
from .plan import Plan
from .subscription import Subscription
from .administration import Administration
#from .administration import Admin
from .agricultural_resource import AgriculturalResource

__all__ = [
    "Base",
    # Core
    "User", "Zone", "Culture", "CalendrierCulture",
    # Diagnostic
    "Diagnostic", "DiagnosticResponse", "AnalyseImage", "ConsultationImage", "Symptome",
    # Conversation / Chatbot
    "Conversation", "Message", "ChatbotIntent", "ChatbotLearning", "ChatbotResource",
    "LearnedPhrase", "Knowledge", "QueryLog",
    # Business
    "Plan", "Subscription", "Administration", "Admin", "AgriculturalResource",
]
