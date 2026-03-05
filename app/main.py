from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import database

# Création de la table au lancement
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Mon API CI/CD")

# Fonction pour obtenir une connexion à la base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/")
def create_task(title: str, db: Session = Depends(get_db)):
    new_task = database.Task(title=title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(database.Task).all()