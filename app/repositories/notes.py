from repositories.alchemy_repo import SQLAlchemyRepository
from models.notes import Notes


class NotesRepo(SQLAlchemyRepository):
    model = Notes
