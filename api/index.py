"""
Vercel serverless function entry point
Adapts FastAPI app for Vercel using Mangum
"""
import sys
import os
from pathlib import Path
import traceback

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set working directory to project root (critical for file paths)
os.chdir(project_root)

try:
    # Import with explicit error handling
    try:
        from server_http import http_app
    except Exception as import_error:
        raise Exception(f"Failed to import server_http: {import_error}")
    
    try:
        from mangum import Mangum
    except Exception as import_error:
        raise Exception(f"Failed to import mangum: {import_error}")
    
    # Create ASGI adapter for Vercel
    handler = Mangum(http_app, lifespan="off")
    
    # Vercel expects 'app' or 'handler'
    app = handler
    
except Exception as e:
    # Enhanced error reporting for debugging
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/{path:path}")
    @error_app.post("/{path:path}")
    async def error_handler(path: str):
        error_details = {
            "error": str(e),
            "error_type": type(e).__name__,
            "path": path,
            "cwd": os.getcwd(),
            "project_root": str(project_root),
            "project_root_exists": project_root.exists(),
            "sys_path": sys.path[:5],  # First 5 entries
            "traceback": traceback.format_exc()
        }
        
        # Check if key files exist
        key_files = [
            "resume.json",
            "rulebook.yaml",
            "b_past_life_mcp/resume.json",
            "northstar_mcp/projects.json"
        ]
        error_details["files"] = {
            f: (project_root / f).exists() for f in key_files
        }
        
        return JSONResponse(error_details, status_code=500)
    
    from mangum import Mangum
    app = Mangum(error_app, lifespan="off")
