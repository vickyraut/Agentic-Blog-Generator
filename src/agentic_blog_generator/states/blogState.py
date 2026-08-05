from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str=Field(description="The title of Blog Post")
    content:str=Field(description="The main content of Blog Post")

class BlogState(TypedDict, total=False):
    topic: str
    blog: Blog
    current_language: str
    blog_length: str


