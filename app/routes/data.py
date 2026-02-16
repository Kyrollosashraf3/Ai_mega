from fastapi import  APIRouter, UploadFile
from app.config.settings import settings

from app.core.file import DataControl

router = APIRouter( prefix="/data" ,   tags=["files"],)

@router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile  ):
    
    # Validate file size, TYPES 
    is_validate =DataControl().validate_uploaded_file(file= file)
    
    
    return {
        " is_validate" : is_validate 
           }
