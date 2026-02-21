from pydantic import BaseModel, Field, validator, BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId
from app.config import settings
from datetime import datetime


# Custom type to handle MongoDB ObjectId as a string in Pydantic
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]


###======== Project =========###

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

    @classmethod
    def get_indexes(cls):
        # index for project_id
        return [
            {
                "key": [ ("project_id", 1) ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]


###======== DataChunk =========###

class DataChunk(BaseModel):
    """ how to save Chunks in Mongo DB"""
    id: Optional[PyObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: str
    chunk_asset_id: PyObjectId

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


    @classmethod
    def get_indexes(cls):
        # index for chunk_project_id
        return [
            {
                "key": [
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "unique": False
            }
        ]


###======== Asset =========###

class Asset(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    asset_project_id: PyObjectId                 # project_id
    asset_name: str = Field(..., min_length=1)   # file_name

    asset_type: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):
        # index for asset_project_id and asset_name together
        return [
            {
                "key": [
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            },
        ]