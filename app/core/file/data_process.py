"""
what we need:  
take file_id >> get extension >> load file with LangChain by path 

so we need to get file_path:  as file_path = project_path + file_id
data_control >  DataControl > get_project_path(self, project_id)

Then Chunking by Recursive Character TextSplitter

functions we need :
get extension , 
load with ext , 
get file content ,
then process + chunking + metadata read

"""


from app.core.file import FileBase , DataControl
from fastapi import UploadFile
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

from app.config import get_logger 
logger = get_logger(__name__)



class DataProcess(FileBase):
    def __init__(self , project_id):
        # call parent FileBase class : super
        super().__init__()
        
        self.project_id = project_id
        self.project_path = DataControl().get_project_path(project_id=project_id)
        
        pass


    def get_extension (self , file_id: str  ): 
            ext = os.path.splitext(file_id)[-1]
            return ext
    
 
    def get_file_loader(self, file_id: str):
        """ select file loader by checking ext"""

        # Get ext and path
        file_ext = self.get_extension(file_id=file_id)

        file_path = os.path.join(
            self.project_path,
            file_id
        )
        
        # check if file exist
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # check ext and load 
        if file_ext == ".txt":
            logger.info(f"load .txt success")
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ".pdf":
            logger.info(f"load .pdf success")
            return PyMuPDFLoader(file_path)
        
        return None


    def get_file_content(self, file_id: str):
        """ use loader to read files """
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            raise ValueError(f"Unsupported file type for file: {file_id}")
            return None
           
        try:
            return loader.load()  # give me List of documents :[file_contents] with text(page_content)_ + metadata >>> export it 
        except Exception as e:
            logger.error(f"Error while loading file - look data route {e}")
            return None


    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100000 , overlap_size: int=100):
        """ create chunks + get matadata """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata   # to give metadate with every chunk 
        )
       # texts = text_splitter.split_text(document)

        return chunks


    