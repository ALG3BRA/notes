from abc import ABC, abstractmethod
from utils.dependencies import UOWDep
from services.notes import NotesService
from services.text_corrector import TextCorrectorService
import uuid
from typing import List
from schemas.notes import NotesSchema  # Предполагается, что у вас есть модель Note


class AbstractNotesUseCase(ABC):

    @abstractmethod
    async def get_notes(self, user_id: uuid.UUID) -> List[NotesSchema]:
        """Retrieve notes for the current user."""
        pass

    @abstractmethod
    async def add_note(self, user_id: uuid.UUID, text: str) -> uuid.UUID:
        """Add a new note for the current user."""
        pass

    @abstractmethod
    async def delete_note(self, user_id: uuid.UUID, note_id: uuid.UUID) -> bool:
        """Delete a note by its ID for the current user."""
        pass

    @abstractmethod
    async def update_note(self, user_id: uuid.UUID, note_id: uuid.UUID, new_text: str) -> bool:
        """Update the text of a note by its ID for the current user."""
        pass

    @abstractmethod
    async def switch_note_status(self, user_id: uuid.UUID, note_id: uuid.UUID) -> bool:
        """Switch the status of a note (e.g., completed, unfinished) for the current user."""
        pass


class NotesUseCase(AbstractNotesUseCase):

    def __init__(self, uow: UOWDep):
        self.uow = uow

    async def get_notes(self, user_id: uuid.UUID) -> List[NotesSchema] | bool:
        async with self.uow as uow:
            try:
                notes = await NotesService.get(uow, user_id)
                if notes is not None:
                    return notes
                return False
            except Exception as err:
                print(err)

    async def add_note(self, user_id: uuid.UUID, text: str) -> uuid.UUID:
        async with self.uow as uow:
            try:
                text = await TextCorrectorService.correct(text)
            except Exception as err:
                print(err)

            note_id = await NotesService.add_one(uow, user_id, text)
            await uow.commit()
            return note_id

    async def delete_note(self, user_id: uuid.UUID, note_id: uuid.UUID) -> bool:
        async with self.uow as uow:
            if await NotesService.delete_one(uow, user_id, note_id):
                await uow.commit()
                return True
            return False

    async def update_note(self, user_id: uuid.UUID, note_id: uuid.UUID, text: str) -> bool:
        async with self.uow as uow:
            try:
                text = await TextCorrectorService.correct(text)
            except Exception as err:
                print(err)
            if await NotesService.update_text(uow, user_id, note_id, text):
                await uow.commit()
                return True
            return False

    async def switch_note_status(self, user_id: uuid.UUID, note_id: uuid.UUID) -> bool:
        async with self.uow as uow:
            new_status = await NotesService.switch_note_status(uow, user_id, note_id)
            await uow.commit()
            return new_status
