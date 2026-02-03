from pydantic import BaseModel
from typing import Optional

class Chat(BaseModel):
    id: int

class Message(BaseModel):
    message_id: int
    chat: Chat
    text: Optional[str] = None

class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None