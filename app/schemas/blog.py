from pydantic import BaseModel


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogUpdate(BaseModel):
    title: str
    content: str
