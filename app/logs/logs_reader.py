import os
from typing import List, Dict, Any
from pathlib import Path

class LogReader:
    def __init__(self, log_path: str = "app/logs/app.log"):
        self.log_path = Path(log_path)

    def get_logs(self, limit: int = 200, level: str = None) -> List[Dict[str, str]]:
        """Reads the log file and returns the last N lines as a list of dictionaries."""
        if not self.log_path.exists():
            return []

        logs = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            # Process lines in reverse to get the latest first
            for line in reversed(lines):
                if not line.strip():
                    continue
                
                # Simple parser based on format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                parts = line.split(" - ", 3)
                if len(parts) >= 4:
                    log_entry = {
                        "timestamp": parts[0],
                        "name": parts[1],
                        "level": parts[2],
                        "message": parts[3].strip()
                    }
                    
                    if level and log_entry["level"] != level:
                        continue
                        
                    logs.append(log_entry)
                    if len(logs) >= limit:
                        break
        except Exception as e:
            return [{"timestamp": "ERROR", "name": "LogReader", "level": "ERROR", "message": str(e)}]

        return logs
