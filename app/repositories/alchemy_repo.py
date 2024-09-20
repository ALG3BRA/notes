import uuid
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Tuple, Optional
from sqlalchemy import insert, desc, delete, asc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from db.postgres import Base

T = TypeVar('T', bound=Base)


class AbstractDatabaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def find_all(self,
                       order_by: Optional[List[str]] = None,
                       limit: Optional[int] = None,
                       **filter_by) -> List[T]:
        pass

    @abstractmethod
    async def add_one(self, **data) -> T:
        pass

    @abstractmethod
    async def delete_by_id(self, id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def update_by_id(self, id: uuid.UUID, **data) -> None:
        pass


class SQLAlchemyRepository(AbstractDatabaseRepository[T]):
    model: type[T] = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def find_all(self,
                       order_by: Optional[Tuple[str]] = None,
                       limit: Optional[int] = None,
                       **filter_by) -> List[T]:

        stmt: Select = select(self.model).filter_by(**filter_by)

        if order_by:
            for column in order_by:
                if column.startswith("-"):
                    stmt = stmt.order_by(desc(getattr(self.model, column[1:])))
                else:
                    stmt = stmt.order_by(asc(getattr(self.model, column)))

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        return [row[0].to_read_model() for row in result.all()]

    async def find_one(self, **filter_by) -> Optional[T]:
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if result:
            result = result.to_read_model()
        return result

    async def add_one(self, **data) -> T:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_by_id(self, id: uuid.UUID, **data) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**data)
        await self.session.execute(stmt)

    async def delete_by_id(self, id: uuid.UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
