from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import auth, blog
from app.db.base import Base
from app.db.session import engine
from app.models.Blogs import Blog
from app.models.user import User

load_dotenv()
Base.metadata.create_all(bind=engine)


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(blog.router)


@app.get("/")
def index():
    return {"message ": "project is running "}
