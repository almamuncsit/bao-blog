import pytest
from sqlalchemy.orm import Session


def test_create_post(client, db_session: Session):
    response = client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Test Content"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_post_with_category(client, db_session: Session):
    # Create a category first
    category_response = client.post(
        "/categories/",
        json={"name": "Test Category"}
    )
    category_id = category_response.json()["id"]

    response = client.post(
        "/posts/",
        json={
            "title": "Test Post with Category",
            "content": "Test Content",
            "category_id": category_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == category_id


def test_create_post_with_invalid_category(client, db_session: Session):
    response = client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Test Content",
            "category_id": 999
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid category ID"


def test_create_post_with_tags(client, db_session: Session):
    # Create tags first
    tag1 = client.post("/tags/", json={"name": "Tag1"})
    tag2 = client.post("/tags/", json={"name": "Tag2"})
    tag_ids = [tag1.json()["id"], tag2.json()["id"]]

    response = client.post(
        "/posts/",
        json={
            "title": "Test Post with Tags",
            "content": "Test Content",
            "tag_ids": tag_ids
        }
    )
    assert response.status_code == 200


def test_create_post_with_invalid_tags(client, db_session: Session):
    response = client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Test Content",
            "tag_ids": [999, 1000]
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "One or more tag IDs are invalid"


def test_read_posts(client, db_session: Session):
    # Create test posts
    client.post("/posts/", json={"title": "Post 1", "content": "Content 1"})
    client.post("/posts/", json={"title": "Post 2", "content": "Content 2"})

    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Post 1"
    assert data[1]["title"] == "Post 2"


def test_read_posts_empty(client, db_session: Session):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_post(client, db_session: Session):
    # Create a post
    create_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Test Content"}
    )
    post_id = create_response.json()["id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"


def test_read_non_existent_post(client, db_session: Session):
    response = client.get("/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_update_post(client, db_session: Session):
    # Create a post
    create_response = client.post(
        "/posts/",
        json={"title": "Original Post", "content": "Original Content"}
    )
    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Post", "content": "Updated Content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Post"
    assert data["content"] == "Updated Content"


def test_update_post_with_tags(client, db_session: Session):
    # Create post and tags
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Test Content"}
    )
    post_id = post_response.json()["id"]

    tag1 = client.post("/tags/", json={"name": "UpdateTag1"})
    tag2 = client.post("/tags/", json={"name": "UpdateTag2"})
    tag_ids = [tag1.json()["id"], tag2.json()["id"]]

    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Post",
            "content": "Updated Content",
            "tag_ids": tag_ids
        }
    )
    assert response.status_code == 200


def test_update_non_existent_post(client, db_session: Session):
    response = client.put(
        "/posts/999",
        json={"title": "Updated Post", "content": "Updated Content"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_delete_post(client, db_session: Session):
    # Create a post
    create_response = client.post(
        "/posts/",
        json={"title": "Delete Post", "content": "Delete Content"}
    )
    post_id = create_response.json()["id"]

    # Delete the post
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully"

    # Verify post is deleted
    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_post(client, db_session: Session):
    response = client.delete("/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"
