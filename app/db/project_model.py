
#from unittest import result
from numpy import insert
from app.config import settings
from app.models.db_schemas import Project

class ProjectModel :

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.settings = settings

        self.collection = self.db_client["projects"]

    
    async def create_project (self , project : Project):

        result = await self.collection.insert_one(project.dict(
                                                        by_alias=True, exclude_unset=True) )
        project.id = str(result.inserted_id)
        # every doc in collection came with _id 
        return project
    
    async def get_project (self, project_id : str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project
        
        record["id"] = str(record["_id"])
        # record is dict >> give it to project model 
        return Project(**record)  