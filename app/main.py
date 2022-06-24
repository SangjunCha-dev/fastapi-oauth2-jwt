from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.admin import admin
from app.api import users, items, login
from app.db.init_db import init_db
from app.db.database import Base, engine, SessionLocal


app = FastAPI(
    title=settings.PROJECT_NAME,
    dependencies=[],
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# database init
Base.metadata.create_all(bind=engine)

def init() -> None:
    '''
    Create first superuser
    '''
    db = SessionLocal()
    init_db(db)

init()


@app.get("/")
async def root():
    return {"message": "Hello World"}
