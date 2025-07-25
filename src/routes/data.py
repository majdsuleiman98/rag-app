from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from controllers import ProjectController
import aiofiles
from models import ResponseSignal
import logging

# Initialize logging
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1","data"])

@data_router.post("/upload/{id}")
async def upload_data(id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    is_valid, message = DataController().validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
    project_root = ProjectController().get_project_root(id)
    key, file_path = ProjectController().generate_unique_filename(file, project_root)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(content)
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseSignal.FILE_UPLOAD_FAILURE.value})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, "key":key})