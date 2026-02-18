from pydantic import BaseModel, Field, validator, BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId
from app.config import settings


# Custom type to handle MongoDB ObjectId as a string in Pydantic
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

class Project(BaseModel):
    """ how to save Project in Mongo DB """

    id: Optional[PyObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)


    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        
        return value

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class DataChunk(BaseModel):
    """ how to save Chunks in Mongo DB"""
    id: Optional[PyObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: str

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True



