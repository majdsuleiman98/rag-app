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
        if not os.path.exists(file_path):
            return None
        if file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        if file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        return None
    
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id)
        if loader:
            return loader.load()
        return None
    
    def process_file_content(self, file_content: list, file_id: str, chunk_size: int=100, overlap_size: int=20):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        texts = [doc.page_content for doc in file_content]
        metadatas = [doc.metadata for doc in file_content]
        chunks = splitter.create_documents(texts, metadatas=metadatas)
        return chunks