from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title= "Note taking app")

app.mount 

templates = Jinja2Templates(directory="UI")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Jaden James",
        "title": "Testing out Fastapi",
        "content": "Well watch ya right, im lowkey fed up of learning how to use this ",
        "date": "Sometime after 8",
    },
    {
        "id": 2,
        "author": "Kamryn Smith",
        "title": "Needed test data",
        "content": "Hey hear joke nuh? BRADAM",
        "date": "Sometime during pan",
    }, 
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/home", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
                    request,
                    "Home.html",
                    # {"posts": posts, "title": "What's poppin for the night"}
                    )   
    

@app.get("/note", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
                    request,
                    "Edit.html")