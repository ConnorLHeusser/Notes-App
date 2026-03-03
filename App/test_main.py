from fastapi.testclient import TestClient
from main import app, notes, get_next_id

client = TestClient(app)


def test_root_returns_hello():
    """Test that the root endpoint returns a welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def test_create_note_api():
    """Test creating a new note via API"""
    initial_count = len(notes)
    
    response = client.post("/api/notes", data={
        "title": "My Test Note",
        "content": "This is the content",
        "author": "Test User"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My Test Note"
    assert data["author"] == "Test User"
    assert len(notes) == initial_count + 1


def test_delete_note_removes_it():
    """Test that deleting a note actually removes it"""
    # First create a note
    create_response = client.post("/api/notes", data={
        "title": "Note to Delete",
        "content": "Delete me"
    })
    note_id = create_response.json()["id"]
    
    # Delete it
    delete_response = client.delete(f"/api/notes/{note_id}")
    assert delete_response.status_code == 200
    
    # Try to get it - should be gone
    get_response = client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 404