from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth


Base.metadata.create_all(bind=engine)
app = FastAPI("title=KT_Demo")

app.include_router(auth.router, prefix="/auth", tags=["auth"])