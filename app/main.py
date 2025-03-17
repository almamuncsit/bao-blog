from fastapi import FastAPI
from .database import engine
from .models import Base
from . import models

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"}
