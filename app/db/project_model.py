
#from unittest import result
from numpy import insert
from app.config import settings
from app.models.db_schemas import Project
from app.config import get_logger


logger = get_logger(__name__)
class ProjectModel :

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.settings = settings

        self.collection = self.db_client[settings.COLLECTION_PROJECT]


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)   # __init__ call 
        await instance.init_collection()
        return instance

    async def init_collection(self):

        # get collection names to check if collection exists
        all_collections = await self.db_client.list_collection_names()   
        if settings.COLLECTION_PROJECT not in all_collections:
            # Create collection if not exists
            self.collection = self.db_client[settings.COLLECTION_PROJECT]
            logger.info("Collection 'projects' created successfully")

            # Create indexes
            indexes = Project.get_indexes()
            try:
                
                for index in indexes:
                    await self.collection.create_index(
                        keys= index["key"],
                        name=index["name"],
                        unique=index["unique"]
                    )
                logger.info("Indexes created successfully")
            except Exception as e:
                logger.error(f"Error creating indexes: {e}")



    
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