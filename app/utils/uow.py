from abc import ABC, abstractmethod
from typing import Any
from db.postgres import async_session_maker
from repositories.notes import NotesRepo
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUOW(ABC):
    notes: NotesRepo

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUOW':
        pass

    @abstractmethod
    async def __aexit__(self, *args: Any) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass


class UOW(AbstractUOW):
    session: AsyncSession
    notes: NotesRepo

    async def __aenter__(self) -> 'UOW':
        self.session = async_session_maker()
        self.notes = NotesRepo(self.session)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
