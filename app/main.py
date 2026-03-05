from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Mon API CI/CD - ToDo List")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schémas Pydantic pour les requêtes et réponses
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    model_config = ConfigDict(from_attributes=True)

# Routes Crud
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = database.Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(database.Task).all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Tâche supprimée avec succès"}