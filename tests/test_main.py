from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# On crée une base de données ISOLÉE pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# On remplace la vraie base par la fausse
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Les tests qui seront lancés par GitHub Actions
def test_create_task():
    response = client.post("/tasks/?title=Faire mon projet CI-CD")
    assert response.status_code == 200
    assert response.json()["title"] == "Faire mon projet CI-CD"

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) > 0