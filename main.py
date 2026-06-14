from fastapi import FastAPI
from db.database import Base, engine
from routers import auth, notes

# Creates all tables in PostgreSQL on startup
# In production you'd use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NotesApp API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])

@app.get("/")
def root():
    return {"message": "NotesApp API is running"}