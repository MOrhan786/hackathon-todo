import sys
import os
import subprocess

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')

# Change to backend directory and run the server
os.chdir(backend_dir)
result = subprocess.run([
    sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'
])

if result.returncode != 0:
    print(f"Server exited with code {result.returncode}")
else:
    print("Server stopped gracefully")