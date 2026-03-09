# MEGA - AI Agent Framework

MEGA is a production-ready AI agent framework built with FastAPI. It features a robust architecture for handling file uploads, data processing (RAG), and persistent storage using MongoDB and vector database Pinecone.

## ✍️ Author
Developed and Maintained by **[Kyrollos Ashraf](https://github.com/Kyrollosashraf3)**


## 🚀 Key Features

- **Asynchronous FastAPI Architecture**: High-performance, non-blocking API handling.
- **File Management**: Support for uploading and processing multiple file types.
- **RAG Data Processing**: Automated chunking, cleaning, and embedding extraction for document-based AI workflows.
- **Vector Search**: Integration with Pinecone for high-speed similarity search.
- **MongoDB Integration**: Permanent storage for projects, assets, and document chunks using Motor.
- **Interactive Log Viewer**: Real-time log monitoring via a dedicated dashboard.
- **Project-based Isolation**: Data is organized and isolated by `project_id`.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Databases**: [MongoDB](https://www.mongodb.com/) (Motor), [Pinecone](https://www.pinecone.io/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **LLM Integration**: OpenAI, Google Gemini, Groq
- **Environment Management**: [pydantic-settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/)

## 📂 Project Structure

```text
Ai_mega/
├── app/
│   ├── config/         # Application settings and logging configuration
│   ├── core/           # Core business logic
│   │   ├── file/       # File processing and management
│   │   ├── llm/        # LLM provider handlers and utilities
│   │   │   ├── families/ # API handlers for major providers (OpenAI, Google, etc.)
│   │   │   └── perplexity/ # specialized perplexity integration
│   │   └── rag/        # RAG pipeline: cleaning and embeddings
│   ├── db/             # Database connection and model repositories
│   ├── logs/           # Log reader and HTML dashboard
│   ├── models/         # Pydantic schemas and data models
│   ├── routes/         # API endpoints (Chat, Data, RAG, Logs, etc.)
│   ├── vectordb/       # Vector database (Pinecone) integration
│   └── main.py         # Application entry point
├── docker/             # Docker configuration and compose files
├── scripts/            # Utility and verification scripts
├── my_files/           # Local storage for physical files
└── requirements.txt    # Project dependencies
```

## 🔌 API Endpoints

### 🩺 Health
- `GET /`: Check application health and version.

### 💬 Chat
- `GET /chat/models`: Retrieve the list of available LLM models and their capabilities.
- `POST /chat/chat`: Send a chat request. Supports both streaming and non-streaming responses.

### 📁 Data & Files
- `POST /data/upload/{project_id}`: Upload a new file for a specific project.
- `POST /process/{project_id}`: Process uploaded files (cleaning -> chunking -> embedding -> Pinecone upsert).
- `DELETE /process/delete/{project_id}`: Remove all processed chunks for a project from MongoDB.

### 🔍 RAG (Retrieval Augmented Generation)
- `POST /rag/search`: Perform similarity search across project documents to retrieve relevant context.

### 📜 Logs
- `GET /logs/view`: Access the interactive HTML log viewer.
- `GET /logs/api`: Fetch structured log data in JSON format.

## ⚙️ Configuration

Create a `.env` file in the root directory based on `.env.example`:

```env
APP_NAME=MEGA
APP_VERSION=0.0.1
MONGODB_URL="mongodb://user:password@localhost:27007"
MONGODB_DATABASE=Ai_mega
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_env
```



## 🎯 What you need to do to use RAG

1.  **Upload a file**: Call `/data/upload/{project_id}` with your `project_id`.
2.  **Process the data**: Run `/process/{project_id}` with the `project_id` and `file_name` to clean, chunk, embed, and store the data in both Pinecone and MongoDB.
3.  **Search**: Run `/rag/search` with your query, `project_id`, and optional `file_ids` to retrieve the most relevant information.

## 🎯 What you need to do to use Chat

1.  **Select a model**: Fetch available models from `/chat/models`.
2.  **Send a message**: Call `/chat/chat` with your chosen model and message history. 
3.  **Streaming (Optional)**: Set `stream: true` to receive real-time token responses.

## 🎯 What you need to do to use Web Search

1.  **Enable Search**: In your `/chat/chat` request, set `web_search_mode` to either `"fast"` or `"deep"`.
2.  **Ask a Question**: Provide your query in the `messages` list as a `user` role.
3.  **Get Enriched Results**: The AI will search the live web and provide a response with source citations in `[URL]` format.



## How To Run

Follow these steps to get the project up and running:

### 1. Infrastructure Setup
Spin up the required services (MongoDB) using Docker:
```bash
cd docker
docker-compose up -d
```

### 2. Environment Setup
Activate your environment and install dependencies:
```bash
# Using Conda
conda activate mega1

# Install requirements
pip install -r requirements.txt
```

### 3. Launch the Application
Start the FastAPI server with auto-reload:
```bash
uvicorn app.main:app --reload
```

### 4. Documentation
Once running, you can access the interactive API docs at:
- **Swagger UI**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`

---
