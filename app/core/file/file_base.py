from app.config import settings
import os 
import string
import random

class FileBase: 

    
    def __init__(self):
        
        self.app_settings = settings

        self.base_dir = settings.FILE_PATH
        self.files_dir = os.path.join(
            self. base_dir,
            "assets/files"
        )
        

    def generate_random_string(self, length: int=5):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
