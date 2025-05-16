from app.db.database import SessionLocal
from sqlalchemy.orm import Session

# Dependency for getting a DB session in a route
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
