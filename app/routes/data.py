from fastapi import  APIRouter, UploadFile , Request
from app.config import settings
from fastapi.responses import JSONResponse
import os
import aiofiles

from app.core.file import DataControl, DataProcess
from app.models import ProcessRequest , DataChunk , Project , Asset
from app.db import ProjectModel , chunkModel , AssetModel

from app.config import get_logger ,signal
logger = get_logger(__name__)



file_router = APIRouter( prefix="/data" ,   tags=["files"])

@file_router.post("/upload/{project_id}")
async def upload_data( request: Request, project_id: str, file: UploadFile  ):
    

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    project = await project_model.get_project( project_id=project_id )


    # Validate file size, TYPES 
    is_validate =DataControl().validate_uploaded_file(file= file)
    if not is_validate:
        return JSONResponse (status_code = 400  ,
                            content = {"is_validate" : is_validate }  )
                            
    # prepare folder - file path with unique file name 
    file_path , file_id = DataControl().generate_unique_filepath( orig_file_name=file.filename,
        project_id=project_id)
    

    # file to chunks >>> save chunk by chunk 
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

    # store asset into db
    asset_model = await AssetModel.create_instance(db_client= request.app.db_client)
    
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type="File",
        as set_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            content={
                "signal": signal.FILE_UPLOAD_SUCCESS.value,
                "file_id": file_id,
                "asset_name" : asset_resource.asset_name,
                "project_id": str (project.id)

            }
        )


data_process_router = APIRouter( prefix="/process" ,   tags=["files"])

@data_process_router.post("/upload/{project_id}")
async def process_tool(request: Request, project_id: str, process_request:ProcessRequest):
   
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model= ProjectModel( db_client= request.app.db_client)
    
    project = await project_model.get_project( project_id= project_id )


    Data_process = DataProcess(project_id = project_id )
    file_content = Data_process.get_file_content(file_id = file_id)


    file_chunks = Data_process.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )



    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=400,
            content={
                "signal": "PROCESSING_FAILED"
            }
        )


    # prepare to insert chunks to mongo 
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]


    chunk_model = await chunkModel.create_instance( db_client=request.app.db_client)

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    no_records = await chunk_model.insert_many_chunks(chunks=  file_chunks_records)  # with batches


    return JSONResponse(
        content={
            "signal": "PROCESSING_SUCCESS",
            "inserted_chunks": no_records
        }
    )


    



data_delete_router = APIRouter( prefix="/process" ,   tags=["files"])

@data_delete_router.delete("/delete/{project_id}")
async def delete_data(request: Request, project_id: str):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_project(project_id=project_id)

    chunk_model =await chunkModel.create_instance(db_client=request.app.db_client)
    no_records = await chunk_model.delete_chunks_by_project_id(
            project_id= project.id
        )
    return JSONResponse(
        content={
            "signal": "DELETE_SUCCESS",
            "deleted_chunks": no_records    
        }
    )