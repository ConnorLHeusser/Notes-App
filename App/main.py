from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uuid
from pyinstrument import Profiler

app = FastAPI(title="Simple Note App")
templates = Jinja2Templates(directory="UI")
notes_db = {}

class Note:
    def __init__(self, title, content, color="#ccd5ae"): 
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.color = color
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.updated_at = self.created_at

# PROFILING ENDPOINT 
@app.middleware("http")
async def profiler_middleware(request: Request, call_next):
    profiler = Profiler(interval=0.000001)
    profiler.start()

    response = await call_next(request)

    profiler.stop()

    print(profiler.output_text())  

    return response


# existing routes
@app.on_event("startup")
async def preload_templates():
    templates.get_template("Notes_Gallery.html")
    templates.get_template("Editor.html")
    
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("Notes_Gallery.html", {"request": request, "notes": notes_db})

@app.get("/new", response_class=HTMLResponse)
async def new_note_page(request: Request):
    return templates.TemplateResponse("Editor.html", {"request": request, "note": None, "is_new": True})

@app.post("/notes/create")
async def create_note(title: str = Form(...), content: str = Form(...), color: str = Form("#ccd5ae")):
    note = Note(title, content, color)
    notes_db[note.id] = note
    return RedirectResponse(url=f"/note/{note.id}", status_code=303)

@app.get("/note/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: str):
    note = notes_db.get(note_id)
    if not note:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("Editor.html", {"request": request, "note": note, "is_new": False})

@app.post("/notes/update/{note_id}")
async def update_note(note_id: str, title: str = Form(...), content: str = Form(...), color: str = Form("#ccd5ae")):
    if note_id in notes_db:
        note = notes_db[note_id]
        note.title = title
        note.content = content
        note.color = color
        note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    return RedirectResponse(url=f"/note/{note_id}", status_code=303)

@app.post("/notes/delete/{note_id}")
async def delete_note(note_id: str):
    if note_id in notes_db:
        del notes_db[note_id]
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "notes_count": len(notes_db)}