import uuid
from typing import Tuple, List, Optional
from utils.uow import AbstractUOW
from schemas.notes import NotesSchema


class NotesService:
    @staticmethod
    async def get(uow: AbstractUOW,
                  user_id: uuid.UUID,
                  order_by: Optional[Tuple[str]] = ("-is_active", "-created_at"),
                  limit: Optional[int] = 1000) -> List[NotesSchema]:
        notes = await uow.notes.find_all(order_by=order_by, limit=limit, user_id=user_id)
        return notes

    @staticmethod
    async def add_one(uow: AbstractUOW, user_id: uuid.UUID, text: str) -> uuid.UUID:
        doc_id = await uow.notes.add_one(user_id=user_id, text=text)
        return doc_id

    @staticmethod
    async def delete_one(uow: AbstractUOW, user_id: uuid.UUID, note_id: uuid.UUID) -> Optional[bool]:
        note = await uow.notes.find_one(id=note_id, user_id=user_id)
        if note:
            await uow.notes.delete_by_id(note_id)
            return True
        return None

    @staticmethod
    async def update_text(uow: AbstractUOW, user_id: uuid.UUID, note_id: uuid.UUID, new_text: str) -> Optional[bool]:
        note = await uow.notes.find_one(id=note_id, user_id=user_id)
        if note:
            await uow.notes.update_by_id(note_id, text=new_text)
            return True
        return None

    @staticmethod
    async def switch_note_status(uow: AbstractUOW, user_id: uuid.UUID, note_id: uuid.UUID) -> Optional[bool]:
        note = await uow.notes.find_one(id=note_id, user_id=user_id)
        if note:
            new_status = not note.is_active
            await uow.notes.update_by_id(id=note_id, is_active=new_status)
            return new_status
        return None
