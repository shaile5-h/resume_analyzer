import os
import sys
import uvicorn

# Ensure the backend directory is in the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    
    print("\n" + "=" * 65)
    print("🚀  AI-Powered Resume Analyzer - Backend Server")
    print(f"📡  API Gateway URL:     http://{host}:{port}")
    print(f"📖  Swagger UI Docs:     http://{host}:{port}/docs")
    print(f"📖  ReDoc UI:            http://{host}:{port}/redoc")
    print(f"🩺  Health Check:        http://{host}:{port}/health")
    print("=" * 65 + "\n")
    
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
