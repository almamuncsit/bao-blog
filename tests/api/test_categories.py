from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from app.main import app
from app.models.category import Category


client = TestClient(app)


def test_create_category(test_db: Session):
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_create_category_without_description(test_db: Session):
    response = client.post(
        "/categories/",
        json={"name": "Test Category"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] is None


def test_create_duplicate_category(test_db: Session):
    # Create first category
    client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    
    # Try to create duplicate
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    assert response.status_code == 400


def test_read_categories(test_db: Session):
    # Create test categories
    client.post("/categories/", json={"name": "Category 1"})
    client.post("/categories/", json={"name": "Category 2"})
    
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Category 1"
    assert data[1]["name"] == "Category 2"


def test_read_categories_empty(test_db: Session):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_category(test_db: Session):
    # Create a category
    create_response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    category_id = create_response.json()["id"]
    
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"


def test_read_non_existent_category(test_db: Session):
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_update_category(test_db: Session):
    # Create a category
    create_response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    category_id = create_response.json()["id"]
    
    # Update the category
    response = client.put(
        f"/categories/{category_id}",
        json={"name": "Updated Category", "description": "Updated Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated Description"


def test_update_non_existent_category(test_db: Session):
    response = client.put(
        "/categories/999",
        json={"name": "Updated Category", "description": "Updated Description"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_delete_category(test_db: Session):
    # Create a category
    create_response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    category_id = create_response.json()["id"]
    
    # Delete the category
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted successfully"
    
    # Verify category is deleted
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_category(test_db: Session):
    response = client.delete("/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"