from fastapi import  APIRouter, UploadFile
from app.config import settings
from fastapi.responses import JSONResponse
import os
import aiofiles
from app.core.file import DataControl

from app.config import get_logger ,signal
logger = get_logger(__name__)


router = APIRouter( prefix="/data" ,   tags=["files"],)

@router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile  ):
    
    # Validate file size, TYPES 
    is_validate =DataControl().validate_uploaded_file(file= file)
    if not is_validate:
        return JSONResponse (status_code = 400  ,
                            content = {"is_validate" : is_validate }  )
                            

    # prepare folder - file path : no Dublication per 
    #project_dir_path= DataControl().get_file_path(project_id = project_id)
    #file_path = os.path.join( project_dir_path,  file.filename )


    # prepare folder - file path with unique file name 
    file_path , file_id = DataControl().generate_unique_filepath( orig_file_name=file.filename,
        project_id=project_id)
    


    # file to chunks >>> save chunck by chunk
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file - look data route {e}")

        return JSONResponse(
            status_code=400,
            content={
                "signal": signal.FILE_UPLOAD_FAILED.value
            }
        )


    return JSONResponse(
            content={
                "signal": signal.FILE_UPLOAD_SUCCESS.value,
               "file_id": file_id
            }
        )

