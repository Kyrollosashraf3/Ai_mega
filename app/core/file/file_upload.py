from app.core.file.file_base import FileBase 
from fastapi import UploadFile
import os
import re

from app.config import get_logger , signal
logger = get_logger(__name__)

class DataControl(FileBase):
    def __init__(self):
        # call parent FileBase class : super
        super().__init__()

    def validate_uploaded_file (self , file: UploadFile):
            
        # Check File Type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            logger.info(f" {signal.FILE_TYPE_NOT_SUPPORTED.value} this file content type is:{file.content_type}")
            return False

        # Check File Size as bytes 
        if file.size > self.app_settings.FILE_ALLOWED_SIZE *1024*1024 : 
            logger.info(f" {signal.FILE_SIZE_EXCEEDED.value} this file size is:{round(file.size/(1028*1028),2)}   MB")
            return False 

        
        logger.info(
            f"{signal.FILE_VALIDATED_SUCCESS.value} "
            f"size: {round(file.size / (1024 * 1024), 2)} MB, "
            f"type: {file.content_type}"
)
        return True


    def generate_unique_filepath (self, orig_file_name: str, project_id ):
        random_key = self.generate_random_string()

        # give random key as unique file name
        clean_file_name = self.get_clean_file_name(orig_file_name  = orig_file_name  )
        file_id = random_key + "_" + clean_file_name

        project_path = self.get_file_path(project_id= project_id)
        new_file_path = os.path.join(project_path,  file_id)
                                  
        
        # chack if this key exists >> generate new one
        if os.path.exists(new_file_path):

            logger.info(f"  find path : {new_file_path} generate a new one ")
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, file_id)
                                   
        return new_file_path , file_id




    def get_clean_file_name(self, orig_file_name: str):
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name




    def get_file_path(self, project_id):
        
        # generate new dir 
        project_dir = os.path.join(
            self.files_dir,
            project_id    )

        # find project_id folder - if not found create one
        if not os.path.exists(project_dir):
            logger.info(f"create new Folder for: {project_id} in:  {project_dir} ")
            os.makedirs(project_dir)
        
        
        return (project_dir)