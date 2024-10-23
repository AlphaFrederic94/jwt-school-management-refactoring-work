# tests/test_app.py
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database.database import Base, get_db
from app.models.user import User
from app.models.grade import Grade

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "student",
        "date_of_birth": "2000-01-01"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

@pytest.mark.asyncio
async def test_login_user(client):
    response = await client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_create_grade(client):
    # First, login to get the access token
    login_response = await client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Create a grade
    response = await client.post("/grades", json={
        "pure_maths": 90.0,
        "chemistry": 85.0,
        "biology": 88.0,
        "computer_science": 92.0,
        "physics": 87.0
    }, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["pure_maths"] == 90.0

@pytest.mark.asyncio
async def test_get_grades_for_student(client):
    # First, login to get the access token
    login_response = await client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Get grades for student
    response = await client.get("/grades/student/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["pure_maths"] == 90.0

@pytest.mark.asyncio
async def test_get_top_students(client):
    # First, login to get the access token
    login_response = await client.post("/auth/login", data={
        "username": "john.doe@example.com",
        "password": "password123"
    })
   
    access_token = login_response.json()["access_token"]

    # Get top students
    response = await client.get("/grades/top-students", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0
