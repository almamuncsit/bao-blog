from fastapi import FastAPI
from .database import engine
from .models import Base
from .api.endpoints import categories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.include_router(categories.router, prefix="/categories", tags=["categories"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"}
