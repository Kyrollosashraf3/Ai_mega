from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
import os
from app.logs.logs_reader import LogReader
from pathlib import Path

router = APIRouter(prefix="/logs", tags=["Logs"])
reader = LogReader()

@router.get("/view", response_class=HTMLResponse)
async def get_logs_view():
    """Returns the HTML view for logs."""
    html_path = Path("app/logs/logs.HTML")
    if not html_path.exists():
        return f"<h1>Logs view not found at {html_path}</h1>", 404
        
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@router.get("/api", response_class=JSONResponse)
async def get_logs_api(limit: int = 200, level: str = None):
    """Returns logs data as JSON."""
    # Handle the case where level is empty string from frontend
    if level == "":
        level = None
    
    logs = reader.get_logs(limit=limit, level=level)
    return logs

# For convenience, also allow access via /api/logs if needed, 
# but prefix /logs is applied to the router.
@router.get("/data", response_class=JSONResponse)
async def get_logs_data(limit: int = 200, level: str = None):
    return reader.get_logs(limit=limit, level=level)
