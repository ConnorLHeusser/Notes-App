import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app, notes, get_next_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_notes():
    """Reset notes to initial state before each test"""
    global notes
    original_notes = notes.copy()
    yield
    notes.clear()
    notes.extend(original_notes)

# ==================== API Tests ====================

class TestAPIEndpoints:
    """Test JSON API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "notes_count" in data

    def test_get_all_notes_api(self):
        """Test GET /api/notes returns all notes"""
        response = client.get("/api/notes")
        assert response.status_code == 200
        data = response.json()
        assert "notes" in data
        assert "count" in data
        assert isinstance(data["notes"], list)

    def test_get_single_note_api_success(self):
        """Test GET /api/notes/{id} with valid ID"""
        response = client.get("/api/notes/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "content" in data

    def test_get_single_note_api_not_found(self):
        """Test GET /api/notes/{id} with invalid ID returns 404"""
        response = client.get("/api/notes/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Note not found"

    def test_create_note_api_success(self):
        """Test POST /api/notes creates a new note"""
        initial_count = len(notes)
        new_note_data = {
            "title": "Test Note API",
            "content": "This is a test note created via API",
            "author": "Test Author",
            "color": "#43e97b"
        }
        
        response = client.post("/api/notes", data=new_note_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == new_note_data["title"]
        assert data["content"] == new_note_data["content"]
        assert data["author"] == new_note_data["author"]
        assert data["color"] == new_note_data["color"]
        assert "id" in data
        assert "created_at" in data
        assert len(notes) == initial_count + 1

    def test_create_note_api_default_values(self):
        """Test POST /api/notes with minimal data uses defaults"""
        response = client.post("/api/notes", data={
            "title": "Minimal Note",
            "content": "Content only"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["author"] == "Anonymous"
        assert data["color"] == "#667eea"

    def test_update_note_api_success(self):
        """Test PUT /api/notes/{id} updates existing note"""
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "color": "#fa709a"
        }
        
        response = client.put("/api/notes/1", data=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["color"] == update_data["color"]

    def test_update_note_api_not_found(self):
        """Test PUT /api/notes/{id} with invalid ID returns 404"""
        response = client.put("/api/notes/9999", data={
            "title": "Test",
            "content": "Test",
            "color": "#ffffff"
        })
        assert response.status_code == 404

    def test_delete_note_api_success(self):
        """Test DELETE /api/notes/{id} removes note"""
        initial_count = len(notes)
        response = client.delete("/api/notes/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Note deleted successfully"
        assert len(notes) == initial_count - 1
        
        # Verify it's actually deleted
        get_response = client.get("/api/notes/1")
        assert get_response.status_code == 404

    def test_delete_note_api_not_found(self):
        """Test DELETE /api/notes/{id} with invalid ID returns 404"""
        response = client.delete("/api/notes/9999")
        assert response.status_code == 404


# ==================== HTML Template Tests ====================

class TestHTMLRoutes:
    """Test HTML template rendering routes"""
    
    def test_home_page(self):
        """Test /home renders Home.html template"""
        response = client.get("/home")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        # Check for expected template content
        assert "My Notes" in response.text or "NoteFlow" in response.text

    def test_new_note_form(self):
        """Test /notes/new renders Editor.html for creation"""
        response = client.get("/notes/new")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Create" in response.text or "New" in response.text

    def test_edit_note_form_success(self):
        """Test /notes/{id}/edit renders Editor.html for existing note"""
        response = client.get("/notes/1/edit")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Edit" in response.text

    def test_edit_note_form_not_found(self):
        """Test /notes/{id}/edit with invalid ID returns 404"""
        response = client.get("/notes/9999/edit")
        assert response.status_code == 404

    def test_legacy_note_route(self):
        """Test /note legacy route still works"""
        response = client.get("/note")
        assert response.status_code == 200


# ==================== Form Submission Tests ====================

class TestFormSubmissions:
    """Test HTML form POST submissions"""
    
    def test_create_note_form_redirect(self):
        """Test POST /notes creates note and redirects"""
        initial_count = len(notes)
        form_data = {
            "title": "Form Test Note",
            "content": "Created via form submission",
            "color": "#4facfe",
            "author": "Form Tester"
        }
        
        response = client.post("/notes", data=form_data, follow_redirects=False)
        assert response.status_code == 303  # Redirect status
        assert response.headers["location"] == "/home"
        assert len(notes) == initial_count + 1

    def test_update_note_form_redirect(self):
        """Test POST /notes/{id} updates note and redirects"""
        form_data = {
            "title": "Updated via Form",
            "content": "Updated content via form",
            "color": "#ffffff"
        }
        
        response = client.post("/notes/1", data=form_data, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/home"
        
        # Verify update
        note = next((n for n in notes if n["id"] == 1), None)
        assert note["title"] == form_data["title"]

    def test_update_note_form_not_found(self):
        """Test POST /notes/{id} with invalid ID returns 404"""
        response = client.post("/notes/9999", data={
            "title": "Test",
            "content": "Test",
            "color": "#ffffff"
        })
        assert response.status_code == 404


# ==================== Helper Function Tests ====================

class TestHelperFunctions:
    """Test utility functions"""
    
    def test_get_next_id_empty_list(self):
        """Test get_next_id when notes list is empty"""
        global notes
        original = notes.copy()
        notes.clear()
        assert get_next_id() == 1
        notes.extend(original)
    
    def test_get_next_id_sequential(self):
        """Test get_next_id returns correct next ID"""
        global notes
        original = notes.copy()
        
        # Add notes with specific IDs
        notes.clear()
        notes.extend([
            {"id": 1, "title": "Test"},
            {"id": 5, "title": "Test"},
            {"id": 3, "title": "Test"}
        ])
        
        assert get_next_id() == 6
        notes.clear()
        notes.extend(original)


# ==================== Integration Tests ====================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_note_lifecycle(self):
        """Test complete CRUD lifecycle of a note"""
        # Create
        create_response = client.post("/api/notes", data={
            "title": "Lifecycle Test",
            "content": "Testing full lifecycle",
            "author": "Integration Test",
            "color": "#43e97b"
        })
        assert create_response.status_code == 200
        created_note = create_response.json()
        note_id = created_note["id"]
        
        # Read
        read_response = client.get(f"/api/notes/{note_id}")
        assert read_response.status_code == 200
        assert read_response.json()["title"] == "Lifecycle Test"
        
        # Update
        update_response = client.put(f"/api/notes/{note_id}", data={
            "title": "Updated Lifecycle Test",
            "content": "Updated content",
            "color": "#fa709a"
        })
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Lifecycle Test"
        
        # Delete
        delete_response = client.delete(f"/api/notes/{note_id}")
        assert delete_response.status_code == 200
        
        # Verify deletion
        verify_response = client.get(f"/api/notes/{note_id}")
        assert verify_response.status_code == 404

    def test_html_form_workflow(self):
        """Test creating note via HTML form and viewing on home page"""
        # Create note via form
        client.post("/notes", data={
            "title": "HTML Workflow Test",
            "content": "Testing HTML workflow",
            "color": "#667eea"
        }, follow_redirects=True)
        
        # Verify it appears on home page
        home_response = client.get("/home")
        assert home_response.status_code == 200
        assert "HTML Workflow Test" in home_response.text


# ==================== Edge Cases ====================

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_create_note_with_empty_title(self):
        """Test creating note with empty title (should handle gracefully)"""
        response = client.post("/api/notes", data={
            "title": "",
            "content": "Content without title"
        })
        # FastAPI Form(...) requires non-empty, but empty string is valid
        assert response.status_code == 200

    def test_create_note_with_special_characters(self):
        """Test creating note with special characters"""
        special_title = "Test <script>alert('xss')</script> & \"quotes\""
        response = client.post("/api/notes", data={
            "title": special_title,
            "content": "Special chars: émojis 🎉 and symbols ©®™"
        })
        assert response.status_code == 200
        # Verify stored correctly (templates should escape HTML)
        data = response.json()
        assert "<script>" in data["title"]  # Stored as-is, escaped in template

    def test_concurrent_note_creation(self):
        """Test creating multiple notes rapidly"""
        initial_id = get_next_id()
        for i in range(5):
            response = client.post("/api/notes", data={
                "title": f"Concurrent Note {i}",
                "content": f"Content {i}"
            })
            assert response.status_code == 200
            assert response.json()["id"] == initial_id + i

    def test_delete_nonexistent_note_idempotent(self):
        """Test deleting same note twice returns 404 second time"""
        # First delete
        client.delete("/api/notes/1")
        # Second delete should fail
        response = client.delete("/api/notes/1")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])