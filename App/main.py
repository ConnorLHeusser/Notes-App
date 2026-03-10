from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from typing import Optional
import os

app = FastAPI(title="Note Taking App")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="UI")

# In-memory notes storage (replace with database in production)
notes: list[dict] = [
    {
        "id": 1,
        "author": "Jaden James",
        "title": "Testing out Fastapi",
        "content": "Well watch ya right, im lowkey fed up of learning how to use this ",
        "created_at": datetime.now(),
        "color": "#667eea"
    },
    {
        "id": 2,
        "author": "Kamryn Smith",
        "title": "Needed test data",
        "content": "Hey hear joke nuh? BRADAM",
        "created_at": datetime.now(),
        "color": "#f093fb"
    },
]

# Helper function to get next ID
def get_next_id() -> int:
    if not notes:
        return 1
    return max(note["id"] for note in notes) + 1

# API Routes (JSON)
@app.get("/")
async def root():
    return {"message": "Hello World", "notes_count": len(notes)}

@app.get("/api/notes")
async def get_notes_api():
    """Get all notes as JSON"""
    return {"notes": notes, "count": len(notes)}

@app.get("/api/notes/{note_id}")
async def get_note_api(note_id: int):
    """Get a specific note as JSON"""
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/api/notes")
async def create_note_api(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form("Anonymous"),
    color: str = Form("#667eea")
):
    """Create a new note via API"""
    new_note = {
        "id": get_next_id(),
        "title": title,
        "content": content,
        "author": author,
        "created_at": datetime.now(),
        "color": color
    }
    notes.append(new_note)
    return new_note

@app.put("/api/notes/{note_id}")
async def update_note_api(
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form(...)
):
    """Update a note via API"""
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note["title"] = title
    note["content"] = content
    note["color"] = color
    return note

@app.delete("/api/notes/{note_id}")
async def delete_note_api(note_id: int):
    """Delete a note via API"""
    global notes
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    notes = [n for n in notes if n["id"] != note_id]
    return {"message": "Note deleted successfully"}

# HTML Template Routes
@app.get("/home", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    """Home page showing all notes (uses Home.html template)"""
    return templates.TemplateResponse(
        request,
        "Home.html",
        {"notes": notes, "title": "My Notes Gallery"}
    )

@app.get("/notes/new", response_class=HTMLResponse, include_in_schema=False)
async def new_note_form(request: Request):
    """Display form to create a new note (uses Editor.html template)"""
    return templates.TemplateResponse(
        request,
        "Editor.html",
        {"note": None, "title": "Create Note"}
    )

@app.get("/notes/{note_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def edit_note_form(request: Request, note_id: int):
    """Display form to edit a note (uses Editor.html template)"""
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return templates.TemplateResponse(
        request,
        "Editor.html",
        {"note": note, "title": "Edit Note"}
    )

@app.post("/notes", response_class=HTMLResponse, include_in_schema=False)
async def create_note_form(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#667eea"),
    author: str = Form("Anonymous")
):
    """Handle form submission to create a new note"""
    new_note = {
        "id": get_next_id(),
        "title": title,
        "content": content,
        "author": author,
        "created_at": datetime.now(),
        "color": color
    }
    notes.append(new_note)
    return RedirectResponse(url="/home", status_code=303)

@app.post("/notes/{note_id}", response_class=HTMLResponse, include_in_schema=False)
async def update_note_form(
    request: Request,
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#667eea")
):
    """Handle form submission to update a note"""
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note["title"] = title
    note["content"] = content
    note["color"] = color
    return RedirectResponse(url="/home", status_code=303)

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    """Delete a note (used by both API and frontend)"""
    global notes
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    notes = [n for n in notes if n["id"] != note_id]
    return {"message": "Note deleted successfully"}

