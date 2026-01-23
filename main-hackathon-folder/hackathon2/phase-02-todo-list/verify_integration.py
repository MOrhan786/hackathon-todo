import subprocess
import time
import requests
import sys

def check_backend_health():
    """Check if the backend server is running and healthy."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def start_backend():
    """Start the backend server in a subprocess."""
    try:
        # Import the app from backend_server module
        import os
        import threading

        # Change to backend directory
        original_dir = os.getcwd()
        backend_dir = os.path.join(original_dir, "backend")

        # Add backend to Python path
        sys.path.insert(0, backend_dir)

        # Start server in a separate thread
        def run_server():
            try:
                from backend_server import app
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
            except Exception as e:
                print(f"Error starting server: {e}")

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait a moment for server to start
        time.sleep(2)

        return True
    except ImportError as e:
        print(f"Could not import backend server: {e}")
        return False

def main():
    print("=== Frontend-Backend Integration Verification ===")

    # Check if backend is already running
    if check_backend_health():
        print("✓ Backend server is already running")
    else:
        print("- Backend server not found, attempting to start...")
        if start_backend():
            # Wait a bit more for the server to start
            time.sleep(3)
            if check_backend_health():
                print("✓ Backend server started successfully")
            else:
                print("✗ Failed to start backend server")
                print("\nTo run the backend manually:")
                print("cd backend && uvicorn backend_server:app --reload")
                return False
        else:
            print("✗ Could not start backend server")
            print("\nTo run the backend manually:")
            print("cd backend && uvicorn backend_server:app --reload")
            return False

    print("\n✓ Integration verification completed!")
    print("The backend server is running and ready for frontend integration.")
    print("\nTo start the frontend:")
    print("cd frontend && npm run dev")

    return True

if __name__ == "__main__":
    main()