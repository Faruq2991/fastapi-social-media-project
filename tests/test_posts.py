import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.database import Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_update_post_authorization(setup_database):
    db = TestingSessionLocal()
    # Create two users
    user1 = models.User(email="user1@example.com", password="password1")
    user2 = models.User(email="user2@example.com", password="password2")
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    # Create a post by user1
    post = models.Post(title="Test Post", content="Content", user_id=user1.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    # Create access tokens
    token_user1 = create_access_token(data={"user_id": user1.id})
    token_user2 = create_access_token(data={"user_id": user2.id})

    # User2 tries to update user1's post - should be forbidden
    response = client.put(
        f"/posts/{post.id}",
        json={"title": "Updated Title", "content": "Updated Content"},
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed to perform this operation"

    # User1 updates their own post - should succeed
    response = client.put(
        f"/posts/{post.id}",
        json={"title": "Updated Title", "content": "Updated Content"},
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"

def test_delete_post_authorization(setup_database):
    db = TestingSessionLocal()
    # Create two users
    user1 = models.User(email="user1delete@example.com", password="password1")
    user2 = models.User(email="user2delete@example.com", password="password2")
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    # Create a post by user1
    post = models.Post(title="Delete Test Post", content="Content", user_id=user1.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    # Create access tokens
    token_user1 = create_access_token(data={"user_id": user1.id})
    token_user2 = create_access_token(data={"user_id": user2.id})

    # User2 tries to delete user1's post - should be forbidden
    response = client.delete(
        f"/posts/{post.id}",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed to perform this operation"

    # User1 deletes their own post - should succeed
    response = client.delete(
        f"/posts/{post.id}",
        headers={"Authorization": f"Bearer {token_user1}"}
    )
    assert response.status_code == 204
