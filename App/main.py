from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uuid
from typing import Optional

app = FastAPI(title="Simple Note App")

# Setup templates and static files
templates = Jinja2Templates(directory="UI")
app.mount("/static", StaticFiles(directory="static"), name="static")


notes_db = {}

# Note model
class Note:
    def __init__(self, title, content, color="#ffffff"):
        self.id = str(uuid.uuid4())[:8]  # Short ID
        self.title = title
        self.content = content
        self.color = color
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.updated_at = self.created_at

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - shows all notes"""
    return templates.TemplateResponse(
        "Notes_Gallery.html", 
        {"request": request, "notes": notes_db}
    )

@app.get("/new", response_class=HTMLResponse)
async def new_note_page(request: Request):
    """New note page"""
    return templates.TemplateResponse(
        "Editor.html", 
        {"request": request, "note": None, "is_new": True}
    )

@app.post("/notes/create")
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#ffffff")
):
    """Create a new note"""
    note = Note(title, content, color)
    notes_db[note.id] = note
    return RedirectResponse(url=f"/note/{note.id}", status_code=303)

@app.get("/note/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: str):
    """View a single note"""
    note = notes_db.get(note_id)
    if not note:
        return RedirectResponse(url="/")
    return templates.TemplateResponse(
        "note_editor.html", 
        {"request": request, "note": note, "is_new": False}
    )

@app.post("/notes/update/{note_id}")
async def update_note(
    note_id: str,
    title: str = Form(...),
    content: str = Form(...),
    color: str = Form("#ffffff")
):
    """Update an existing note"""
    if note_id in notes_db:
        note = notes_db[note_id]
        note.title = title
        note.content = content
        note.color = color
        note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    return RedirectResponse(url=f"/note/{note_id}", status_code=303)

@app.post("/notes/delete/{note_id}")
async def delete_note(note_id: str):
    """Delete a note"""
    if note_id in notes_db:
        del notes_db[note_id]
    return RedirectResponse(url="/", status_code=303)