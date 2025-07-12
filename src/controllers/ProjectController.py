from .BaseController import BaseController
from fastapi import UploadFile

import os
import uuid

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_root(self, project_id: str) -> str:
        project_path = os.path.join(self.files_root, project_id)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return project_path
    
    def generate_unique_filename(self, file: UploadFile, project_root: str):
        _, file_ext = os.path.splitext(file.filename)
        key = uuid.uuid4().hex
        unique_filename = f"{key}{file_ext}"
        file_path = f"{project_root}/{unique_filename}"
        return key, file_path
