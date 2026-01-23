import subprocess
import sys
import time
import requests

def start_backend():
    # Start the backend server
    print("Starting backend server...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "main:app", "--host", "0.0.0.0", "--port", "8000"
    ], cwd="backend")

    # Give the server some time to start
    time.sleep(5)

    # Test if the server is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend server is running and responding")
            return process
        else:
            print(f"✗ Backend server responded with status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("✗ Backend server is not responding")
        return None

if __name__ == "__main__":
    server_process = start_backend()
    if server_process:
        print("Backend server started successfully. Press Ctrl+C to stop.")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
            server_process.wait()
    else:
        print("Failed to start backend server")