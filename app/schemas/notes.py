from pydantic import BaseModel
from datetime import datetime
import uuid


class NotesSchema(BaseModel):
    id: uuid.UUID
    text: str
    is_active: bool
    created_at: datetime
