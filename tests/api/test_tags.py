import pytest
from sqlalchemy.orm import Session


def test_create_tag(client, db_session: Session):
    response = client.post(
        "/tags/",
        json={"name": "Test Tag"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Tag"
    assert "id" in data


def test_create_duplicate_tag(client, db_session: Session):
    # Create first tag
    client.post(
        "/tags/",
        json={"name": "Duplicate Tag"}
    )
    
    # Try to create duplicate
    response = client.post(
        "/tags/",
        json={"name": "Duplicate Tag"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Tag with this name already exists"


def test_read_tags(client, db_session: Session):
    # Create test tags
    client.post("/tags/", json={"name": "Tag 1"})
    client.post("/tags/", json={"name": "Tag 2"})
    
    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Tag 1"
    assert data[1]["name"] == "Tag 2"


def test_read_tags_empty(client, db_session: Session):
    response = client.get("/tags/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_tag(client, db_session: Session):
    # Create a tag
    create_response = client.post(
        "/tags/",
        json={"name": "Single Test Tag"}
    )
    tag_id = create_response.json()["id"]
    
    response = client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Test Tag"


def test_read_non_existent_tag(client, db_session: Session):
    response = client.get("/tags/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_update_tag(client, db_session: Session):
    # Create a tag
    create_response = client.post(
        "/tags/",
        json={"name": "Update Test Tag"}
    )
    tag_id = create_response.json()["id"]
    
    # Update the tag
    response = client.put(
        f"/tags/{tag_id}",
        json={"name": "Updated Tag"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Tag"


def test_update_tag_duplicate_name(client, db_session: Session):
    # Create two tags
    client.post("/tags/", json={"name": "Existing Tag"})
    create_response = client.post("/tags/", json={"name": "Tag to Update"})
    tag_id = create_response.json()["id"]
    
    # Try to update second tag with first tag's name
    response = client.put(
        f"/tags/{tag_id}",
        json={"name": "Existing Tag"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Tag with this name already exists"


def test_update_non_existent_tag(client, db_session: Session):
    response = client.put(
        "/tags/999",
        json={"name": "Updated Tag"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_delete_tag(client, db_session: Session):
    # Create a tag
    create_response = client.post(
        "/tags/",
        json={"name": "Delete Test Tag"}
    )
    tag_id = create_response.json()["id"]
    
    # Delete the tag
    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Tag deleted successfully"
    
    # Verify tag is deleted
    get_response = client.get(f"/tags/{tag_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_tag(client, db_session: Session):
    response = client.delete("/tags/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"