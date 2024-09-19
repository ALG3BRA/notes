import uuid
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from schemas.notes import NotesSchema
from usecases.dependencies import NotesCase
from utils.auth import current_active_user

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/")
async def get_notes(notes_case: NotesCase, user=Depends(current_active_user)):
    return await notes_case.get_notes(user.id)


@router.post("/")
async def add_note(text: str, notes_case: NotesCase, user=Depends(current_active_user)):
    note_id = await notes_case.add_note(user.id, text)
    if note_id:
        return JSONResponse(status_code=201,
                            content={
                                "message": "Note added successfully",
                                "note_id": str(note_id)
                            })


@router.patch("/{note_id}")
async def update_text(note_id: uuid.UUID, text: str, notes_case: NotesCase, user=Depends(current_active_user)):
    if await notes_case.update_note(user.id, note_id, text):
        return JSONResponse(status_code=204, content={"message": "Note updated successfully"})
    return HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}")
async def delete_note(note_id: uuid.UUID, notes_case: NotesCase, user=Depends(current_active_user)):
    if await notes_case.delete_note(user.id, note_id):
        return JSONResponse(status_code=204, content={"message": "Note deleted successfully"})
    return HTTPException(status_code=404, detail="Note not found")


@router.patch("/status/{note_id}")
async def switch_status(note_id: uuid.UUID, notes_case: NotesCase, user=Depends(current_active_user)):
    print(note_id)
    new_status = await notes_case.switch_note_status(user.id, note_id)
    if new_status is not None:
        return JSONResponse(status_code=200,
                            content={
                                "message": "Note status switched successfully",
                                "status": new_status
                            })

    return HTTPException(status_code=404, detail="Note not found")
