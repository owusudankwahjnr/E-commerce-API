from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db

router = APIRouter()

@router.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Welcome to the E-Commerce API with DB Connected"}

