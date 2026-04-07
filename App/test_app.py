import requests
import time
from pyinstrument import Profiler

def test_profiling_with_query_param():
    """Test profiling using query parameter"""
    
    base_url = "http://localhost:8000"
    
    print("="*60)
    print("Testing with ?profile=true query parameter")
    print("="*60)
    
    # Make request with profiling enabled
    response = requests.get(f"{base_url}/?profile=true")
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response length: {len(response.text)}")
    
    # Check for profile file in output
    import os
    profile_files = [f for f in os.listdir(".") if f.startswith("profile_") and f.endswith(".html")]
    if profile_files:
        print(f"\n✅ Profile files created:")
        for pf in profile_files[-3:]:  # Show last 3
            print(f"   - {pf}")

def test_profile_endpoint():
    """Test the dedicated profile endpoint"""
    
    print("\n" + "="*60)
    print("Testing /profile-request endpoint")
    print("="*60)
    
    response = requests.get("http://localhost:8000/profile-request")
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"Response length: {len(response.text)}")
    
    # Save the profile HTML
    with open("manual_profile.html", "w") as f:
        f.write(response.text)
    print("✅ Profile saved to: manual_profile.html")

def test_custom_profile():
    """Test custom operation profiling"""
    
    print("\n" + "="*60)
    print("Testing /profile-custom/create_note endpoint")
    print("="*60)
    
    # First create some notes
    print("Creating notes...")
    for i in range(10):
        response = requests.post(
            "http://localhost:8000/notes/create",
            data={
                "title": f"Profile Test Note {i}",
                "content": "This is test content " * 50,
                "color": "#ccd5ae"
            }
        )
    
    print("Profiling note creation...")
    response = requests.get("http://localhost:8000/profile-custom/create_note")
    with open("create_note_profile.html", "w") as f:
        f.write(response.text)
    print("✅ Profile saved to: create_note_profile.html")
    
    print("\nProfiling note listing...")
    response = requests.get("http://localhost:8000/profile-custom/list_notes")
    with open("list_notes_profile.html", "w") as f:
        f.write(response.text)
    print("✅ Profile saved to: list_notes_profile.html")

def profile_without_server():
    """Profile code directly without running server"""
    
    print("\n" + "="*60)
    print("Profiling directly with pyinstrument")
    print("="*60)
    
    profiler = Profiler()
    profiler.start()
    
    # Simulate note creation
    notes = []
    for i in range(1000):
        note = {
            "id": i,
            "title": f"Note {i}",
            "content": "X" * 100,
            "created_at": time.time()
        }
        notes.append(note)
    
    # Simulate searching
    search_results = []
    search_term = "Note"
    for note in notes:
        if search_term in note["title"]:
            search_results.append(note)
    
    # Simulate sorting
    sorted_notes = sorted(notes, key=lambda x: x["created_at"], reverse=True)
    
    profiler.stop()
    
    # Print to console
    profiler.print()
    
    # Save to HTML
    with open("direct_profile.html", "w") as f:
        f.write(profiler.output_html())
    print("✅ Profile saved to: direct_profile.html")

if __name__ == "__main__":
    # First make sure server is running
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("Run: python -m uvicorn main:app --reload\n")
    
    input("Press Enter to continue...")
    
    # Run tests
    test_profiling_with_query_param()
    test_profile_endpoint()
    test_custom_profile()
    profile_without_server()
    
    print("\n" + "="*60)
    print("✅ All profiling tests complete!")
    print("📊 Check the generated HTML files for visual profiles")
    print("="*60)