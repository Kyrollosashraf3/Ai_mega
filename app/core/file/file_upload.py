from app.core.file.file_base import FileBase
from fastapi import  UploadFile

class DataControl(FileBase):
    def __init__(self):
        # call parent FileBase class : super
        super().__init__()


    def validate_uploaded_file (self , file : UploadFile):
            
        # Check File Type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False

        # Check File Size as bytes 
        if file.size > self.app_settings.FILE_ALLOWED_SIZE *1024*1024 : 
            return False 
        
        return True
