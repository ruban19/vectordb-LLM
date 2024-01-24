from pydantic import BaseModel, Field, ValidationError
from typing import List,Any
from datetime import datetime, timezone
from pydantic import BaseModel, validator
import pydantic


class SearchRequest(BaseModel):
    text: str = Field(None,description="The text to do similarity search with the Vector Database",max_length=300)


class upsert_model(BaseModel):
    id: int = Field(description="The primary key of the table")
    embedding: List[float]
    text: str
    created_at: str

class delete_model(BaseModel):
    id: int = Field(description="The primary key of the table which has tp be deleted from the table")