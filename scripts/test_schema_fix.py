import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.models.db_schemas import Project
from bson import ObjectId

def test_project_validation():
    print("Testing Project model validation with ObjectId...")
    
    # Simulate a record from MongoDB
    mongodb_record = {
        "_id": ObjectId("69961cffdee874595bd8a6ee"),
        "project_id": "testproject123"
    }
    
    try:
        project = Project(**mongodb_record)
        print("Success! Project instantiated correctly.")
        print(f"Project ID (aliased): {project.id}")
        print(f"Project ID type: {type(project.id)}")
        assert isinstance(project.id, str)
        assert project.id == str(mongodb_record["_id"])
    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_project_validation()
