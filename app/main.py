import os
import sys

# Force SQLite for testing - THIS MUST BE FIRST!
if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    from unittest.mock import patch
    patch.dict(os.environ, {"DATABASE_URL": "sqlite:///./test.db"}).start()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # ← Add this line
from app.database import engine, get_db, Base
from app.models import Student
from pydantic import BaseModel
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic model for request/response
class StudentCreate(BaseModel):
    reg_no: str
    name: str
    email: str

class StudentResponse(BaseModel):
    id: int
    reg_no: str
    name: str
    email: str

# Registration number
YOUR_REG_NO = "2212183"

from sqlalchemy import text  # Add this import at the top of the file

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        print(f"Health check error: {e}")
        db_status = "disconnected"
    
    return {
        "status": "ok",
        "db": db_status,
        "student": YOUR_REG_NO
    }

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.reg_no == student.reg_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Registration number already exists")
    
    db_student = Student(reg_no=student.reg_no, name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{reg_no}")
def get_student_by_reg(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.reg_no == reg_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student