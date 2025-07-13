from .BaseController import BaseController
import os
from models import ProcessingEnums
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = os.path.join(self.files_root, self.project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):
        file_extension = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)
        if file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        if file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path, encoding="utf-8")
        return None
    
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id)
        return loader.load()
    
    def process_file_content(self, file_content: list, file_id: str, chunk_size: int=100, overlap_size: int=20):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        text = [file_content[0].page_content]
        metadata = [file_content[0].metadata]
        chunks = splitter.create_documents(text, metadatas=metadata)
        return chunks