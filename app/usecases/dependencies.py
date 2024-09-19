from typing import Annotated
from fastapi import Depends
from usecases.notes import AbstractNotesUseCase, NotesUseCase

NotesCase = Annotated[AbstractNotesUseCase, Depends(NotesUseCase)]
