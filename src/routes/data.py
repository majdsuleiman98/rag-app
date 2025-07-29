from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes.Chunk import Chunk
from models.db_schemes.Asset import Asset
from models.enums.AssetEnum import AssetEnums
import os
# Initialize logging
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1","data"])

@data_router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    is_valid, message = DataController().validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": message}
            )
    project_root = ProjectController().get_project_root(project_id)
    file_id, file_path = ProjectController().generate_unique_filename(file, project_root)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(content)
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": ResponseSignal.FILE_UPLOAD_FAILURE.value}
            )
    asset_model = await AssetModel.create_instance(db_client= request.app.db_client)
    asset_recource = Asset(asset_project_id=project.id, 
                            asset_type=AssetEnums.ASSET_TYPE.value,
                            asset_name=file_id, 
                            asset_size=os.path.getsize(file_path)
                            )
    _ = await asset_model.create_asset(asset_recource)
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, 
        "file_id":file_id, 
        "project_id":str(project.id)}
        )

@data_router.post("/process/{project_id}")
async def process_data(request: Request, project_id: str, process_request: ProcessRequest):
    #file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    project_file_ids = dict()
    #if process_request.file_id:
    #    project_file_ids = [process_request.file_id]
    #else:
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    project_files = await asset_model.get_all_project_assets(asset_project_id=project.id, asset_type=AssetEnums.ASSET_TYPE.value)
    project_file_ids = {rec.id: rec.asset_name for rec in project_files}
    if len(project_files) == 0:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": ResponseSignal.NO_FILES_ERROR.value}
                )
    process_controller = ProcessController(project_id=project_id)
    number_of_records = 0
    number_of_files = 0
    chunk_model = await ChunkModel.create_instance(db_client= request.app.db_client)
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(project.id)
    for asset_id, file_id in project_file_ids.items():
        file_content = process_controller.get_file_content(file_id)
        if file_content is None:
            logger.error("file no found")
            continue
        chunks = process_controller.process_file_content(file_content, file_id, chunk_size, overlap_size)
        if chunks is None or len(chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"message": ResponseSignal.FILE_PROCESSONG_FAILURE.value}
                )
        chunks_records = [
            Chunk(
                chunk_text= chunk.page_content,
                chunk_metadata= chunk.metadata,
                chunk_order= i+1,
                chunk_project_id= project.id,
                chunk_asset_id=asset_id,
                )
        for i, chunk in enumerate(chunks)
        ]
        
        number_of_records += await chunk_model.insert_many_chunks(chunks=chunks_records, batch_size=64)
        number_of_files +=1

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={
            "message": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
            "inserted_chunks":number_of_records, 
            "processed_files":number_of_files
            })