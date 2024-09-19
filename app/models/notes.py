from sqlalchemy import UUID, Column, String, TIMESTAMP, Boolean, func, ForeignKey
from models.base import Base
from schemas.notes import NotesSchema
import uuid


class Notes(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)

    def to_read_model(self):
        return NotesSchema(
            id=self.id,
            text=self.text,
            is_active=self.is_active,
            created_at=self.created_at
        )
