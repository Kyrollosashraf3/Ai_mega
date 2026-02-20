
#from unittest import result
from numpy import insert
from app.config import settings
from app.models.db_schemas import Asset
from app.config import get_logger


logger = get_logger(__name__)


class AssetModel :

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.settings = settings

        self.collection = self.db_client[settings.COLLECTION_ASSET]


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)   # __init__ call 
        await instance.init_collection()
        return instance


    async def init_collection(self):

        # get collection names to check if collection exists
        all_collections = await self.db_client.list_collection_names()   
        if settings.COLLECTION_ASSET not in all_collections:
            # Create collection if not exists
            self.collection = self.db_client[settings.COLLECTION_ASSET]
            logger.info("Collection 'assets' created successfully")

            # Create indexes
            indexes = Asset.get_indexes()
            try:
                for index in indexes:
                    await self.collection.create_index(
                        key= index["key"],
                        name=index["name"],
                        unique=index["unique"]
                    )
                logger.info("Indexes created successfully")
            except Exception as e:
                logger.error(f"Error creating indexes: {e}")



    
    async def create_asset (self , asset : Asset):

        result = await self.collection.insert_one(asset.dict(
                                                        by_alias=True, exclude_unset=True) )
        asset.id = str(result.inserted_id)
        # every doc in collection came with _id 
        logger.info(f" insert asset success: {asset.asset_name}")

        return asset
    
    async def get_asset (self, asset_project_id : str):

        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
        }).to_list(length=None) # get all
