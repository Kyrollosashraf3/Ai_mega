
#from unittest import result
from bson import ObjectId

from numpy import insert
from app.config import settings
from app.models.db_schemas import DataChunk
from pymongo import InsertOne  # collect chunks into bulks 

class chunkModel :

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.settings = settings

        self.collection = self.db_client["chunk"]

    
    async def create_chunk (self , chunk : DataChunk):

        result = await self.collection.insert_one(chunk.dict(
                                                    by_alias=True, exclude_unset=True) ) 
        # db deals with dict As id= _id , 
        chunk.id = str(result.inserted_id)
        # every doc in collection came with _id 
        return chunk
    

    async def get_chunk (self, chunk_id : str):

        record = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if record is None:
            return None

        record["_id"] = str(record["_id"])
        # record is dict >> give it to DataChunk model 
        return DataChunk(**record)  
    

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        """make batch of set of chunks as bulk insted of insert them all at once"""

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]

            # prepare insert operation ->> give it to mongo with bulk_write 
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)
        
        return len(chunks)
    
    
    async def delete_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count
    
    