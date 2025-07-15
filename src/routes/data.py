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
from models.db_schemes.Chunk import Chunk

# Initialize logging
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1","data"])

@data_router.post("/upload/{id}")
async def upload_data(request: Request, id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=id)
    is_valid, message = DataController().validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
    project_root = ProjectController().get_project_root(id)
    file_id, file_path = ProjectController().generate_unique_filename(file, project_root)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(content)
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseSignal.FILE_UPLOAD_FAILURE.value})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, "file_id":file_id, "project_id":str(project._id)})

@data_router.post("/process/{id}")
async def process_data(request: Request, id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    project_model = await ProjectModel.create_instance(db_client= request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=id)
    process_controller = ProcessController(project_id=id)
    file_content = process_controller.get_file_content(file_id)
    chunks = process_controller.process_file_content(file_content, file_id, chunk_size, overlap_size)
    if chunks is None or len(chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseSignal.FILE_PROCESSONG_FAILURE.value})
    
    chunks_records = [
        Chunk(
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata,
            chunk_order= i+1,
            chunk_project_id= project.id
        )
        for i, chunk in enumerate(chunks)
    ]
    chunk_model = await ChunkModel.create_instance(db_client= request.app.db_client)
    if do_reset == 1:
        _ =await chunk_model.delete_chunks_by_project_id(project.id)
    number_of_records = await chunk_model.insert_many_chunks(chunks=chunks_records, batch_size=64)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.FILE_PROCESSING_SUCCESS.value, "inserted_chunks":number_of_records})