from fastapi import FastAPI
from .database import engine
from .models import Base
from .api.endpoints import categories, tags

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"}
