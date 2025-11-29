import pytest
from fastapi.testclient import TestClient
from app.database import get_db
from ..main import app # Import your app
from .test_database import override_get_db, test_engine, Base  # Test DB setup
# from ..models import Author, Book

# Override DB dependency for all tests
app.dependency_overrides[get_db] = override_get_db # Wait, app.get_db? No: it's your get_db function
# Correct: app.dependency_overrides[get_db] = override_get_db # Fix this in code

# Client for making API calls
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Reset DB before each test
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_create_author():
    response = client.post("/authors/", json={"name": "Test Author3"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Author3"
    assert "id" in data

def test_read_authors():
    # First create one
    client.post("/authors/", json={"name": "Author1"})
    response = client.get("/authors/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_read_author():
    # Create
    create_res = client.post("/authors/", json={"name": "Author2"})
    author_id = create_res.json()["id"]
    # Read
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Author2"

def test_update_author():
    # Create
    create_res = client.post("/authors/", json={"name": "Old Name"})
    author_id = create_res.json()["id"]
    # Update
    response = client.put(f"/authors/{author_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_delete_author():
    # Create
    create_res = client.post("/authors/", json={"name": "To Delete"})
    author_id = create_res.json()["id"]
    # Delete
    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Author deleted"
    # Verify gone
    get_res = client.get(f"/authors/{author_id}")
    assert get_res.status_code == 404

# Similar tests for Books (symmetric to Authors)
def test_create_book():
    # First create author
    author_res = client.post("/authors/", json={"name": "Book Author"})
    author_id = author_res.json()["id"]
    # Create book
    response = client.post("/books/", json={"title": "Test Book", "author_id": author_id})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author_name"] == "Book Author"

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200

def test_read_book():
    # Create author & book
    author_res = client.post("/authors/", json={"name": "Book Author2"})
    author_id = author_res.json()["id"]
    book_res = client.post("/books/", json={"title": "Book2", "author_id": author_id})
    book_id = book_res.json()["id"]
    # Read
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Book2"

def test_update_book():
    # Create author & book
    author_res = client.post("/authors/", json={"name": "Update Author"})
    author_id = author_res.json()["id"]
    book_res = client.post("/books/", json={"title": "Old Title", "author_id": author_id})
    book_id = book_res.json()["id"]
    # Update
    response = client.put(f"/books/{book_id}", json={"title": "New Title", "author_id": author_id})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_book():
    # Create author & book
    author_res = client.post("/authors/", json={"name": "Delete Author"})
    author_id = author_res.json()["id"]
    book_res = client.post("/books/", json={"title": "To Delete", "author_id": author_id})
    book_id = book_res.json()["id"]
    # Delete
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    # Verify gone
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404