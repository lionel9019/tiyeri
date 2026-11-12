# backend/conversations/schemas.py

from pydantic import BaseModel
from datetime import datetime
 
class ConversationBase(BaseModel):
    user_id: int
    message: str

class ConversationCreate(ConversationBase):
    pass

class ConversationOut(ConversationBase):
    id: int
    user_id: int
    titre: str
    created_at: datetime

   # id: int
   # timestamp: datetime

    class Config:
        #orm_mode = True
        from_attributes = True

# backend/conversations/schemas.py

class ConversationWithLastMessage(BaseModel):
    id: int
    user_id: int
    titre: str
    created_at: datetime
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
