from pydantic import BaseModel, Field
from typing import List

class BlogOutline(BaseModel):
    title: str = Field(description="A catchy, engaging blog post title")
    intro: str = Field(description="A two sentence introduction for the blog post")
    sections: List[str] = Field(description="A list of section headings for the blog post")
