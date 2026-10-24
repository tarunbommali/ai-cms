"""
Backend startup script
Initializes database and starts the FastAPI server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db
import uvicorn


def main():
    """Initialize and start the backend"""
    print("=" * 60)
    print("🚀 Artificial Intelligent Cloud Monitoring System - Backend Server")
    print("=" * 60)
    
    # Initialize database
    print("\n📦 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Start server
    print("\n🌐 Starting FastAPI server...")
    print("📍 API Documentation: http://localhost:8000/api/docs")
    print("📍 Alternative Docs: http://localhost:8000/api/redoc")
    print("📍 Health Check: http://localhost:8000/api/health")
    print("\n💡 Tip: Run 'python create_dummy_users.py' to create test users")
    print("=" * 60)
    print("\n")
    
    # Start uvicorn server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
