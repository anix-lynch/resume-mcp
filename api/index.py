"""
Vercel serverless function entry point
Adapts FastAPI app for Vercel using Mangum
"""
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set working directory to project root
os.chdir(project_root)

try:
    from server_http import http_app
    from mangum import Mangum
    
    # Create ASGI adapter for Vercel
    handler = Mangum(http_app, lifespan="off")
    
    # Vercel expects 'app' or 'handler'
    app = handler
    
except Exception as e:
    # Fallback for debugging
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/{path:path}")
    async def error_handler(path: str):
        return JSONResponse({
            "error": str(e),
            "path": path,
            "cwd": os.getcwd(),
            "sys_path": sys.path
        }, status_code=500)
    
    from mangum import Mangum
    app = Mangum(error_app, lifespan="off")
