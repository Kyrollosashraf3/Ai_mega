# MEGA - AI Agent Framework

MEGA is a production-ready AI agent framework built with FastAPI. It features a robust architecture for handling file uploads, data processing (RAG), and persistent storage using MongoDB.

## 🚀 Key Features

- **Asynchronous FastAPI Architecture**: High-performance, non-blocking API handling.
- **File Management**: Support for uploading and processing `text/plain` and `application/pdf` files.
- **RAG Data Processing**: Automated chunking and metadata extraction for document-based AI workflows.
- **MongoDB Integration**: Permanent storage for projects and document chunks using Motor (async driver).
- **Custom Schema Validation**: Robust Pydantic models with custom validators for handling MongoDB ObjectIds.
- **Project-based Isolation**: Data is organized and isolated by `project_id`.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [MongoDB](https://www.mongodb.com/) (using [Motor](https://motor.readthedocs.io/))
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **File Handling**: [aiofiles](https://github.com/Tinche/aiofiles)
- **Environment Management**: [pydantic-settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/)

## 📂 Project Structure

```text
Ai_mega/
├── app/
│   ├── config/         # Application settings and logging
│   ├── core/           # Core logic for file processing
│   ├── db/             # Database models and clients
│   ├── models/         # Pydantic/Database schemas
│   ├── routes/         # API endpoints (Chat, Data, Base)
│   └── main.py         # Application entry point
├── scripts/            # Utility and verification scripts
├── my_files/           # local storage for uploaded files
└── requirements.txt    # Project dependencies
```

## 🔌 API Endpoints

### Health Check
- `GET /`: Check application health and version.

### Chat
- `GET /chat/`: Welcome endpoint for the chat service.

### Data & Files
- `POST /data/upload/{project_id}`: Upload a new file for a project.
- `POST /process/upload/{project_id}`: Process an uploaded file into chunks.
- `DELETE /process/delete/{project_id}`: Delete all processed chunks associated with a project.

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
APP_NAME=MEGA
APP_VERSION=0.0.1
MONGODB_URL= "mongodb://user:password@localhost:27007"
MONGODB_DATABASE=Ai_mega
DEBUG=True
```

## 🏃 Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - Redoc: `http://localhost:8000/redoc`




   ## MongoDB
   we have 2 collections : 
   1- projects : 
   2- chunks : 

   they connected with project_id : that _id of project = chunks.project_id  
   
      

   WITH username and password

   ## docker 

   docker-compose up -d  
   it has : mongodb servise as vertual network with image mongo:7-jammy
   with ROOT_USERNAM and ROOT_PASSWORD from .env file 



# To Run
- cd docker
- docker-compose up -d

- conda activate mega1
- uvicorn app.main:app --reload




-------------
# <span style="color:orange">   RAG     </span>

## 1- route/data
### endpoint 1 
upload file > save content in Mongo db
### endpoint 2
process file take file from mongo db > chunck > embedding > save in vector db Pinecone 
### endpoint 3
delete file chuncks

## 2- route/doctument
### endpoint 1
store chunck vector  > get chuncks from mongo db to embedding and store in vector db Pinecone 

### endpoint 2
take message , file_id or project_id > retrieve top k answers from vector db Pinecone 

### endpoint 3
same idea in chat request to retrieve answeres > put it with LLM Prompt