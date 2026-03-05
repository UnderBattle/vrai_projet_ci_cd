from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Tests
def test_create_task():
    response = client.post("/tasks/", json={"title": "Faire le CRUD", "description": "C'est important"})
    assert response.status_code == 200, response.text
    assert response.json()["title"] == "Faire le CRUD"
    assert not response.json()["completed"]

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200, response.text
    assert type(response.json()) is list

def test_update_task():
    create_resp = client.post("/tasks/", json={"title": "Tâche à modifier"})
    assert create_resp.status_code == 200, create_resp.text
    task_id = create_resp.json()["id"]

    update_resp = client.put(f"/tasks/{task_id}", json={"completed": True})
    assert update_resp.status_code == 200, update_resp.text
    assert update_resp.json()["completed"]

def test_delete_task():
    create_resp = client.post("/tasks/", json={"title": "Tâche à supprimer"})
    assert create_resp.status_code == 200, create_resp.text
    task_id = create_resp.json()["id"]

    del_resp = client.delete(f"/tasks/{task_id}")
    assert del_resp.status_code == 200, del_resp.text

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404