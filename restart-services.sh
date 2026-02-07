#!/bin/bash

# Restart Services Script for Phase-03 Todo List
# This script stops old processes and starts fresh instances

set -e

echo "🔄 Restarting Phase-03 Todo List Services..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to kill processes on a specific port
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null || true)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}Stopping process on port $port${NC}"
        kill -9 $pids 2>/dev/null || true
        sleep 1
    fi
}

# Step 1: Stop old backend processes
echo -e "${YELLOW}Step 1: Stopping old backend processes...${NC}"
kill_port 8000

# Also kill any uvicorn processes from phase-02
pkill -f "phase-02.*uvicorn" || true
sleep 2

# Step 2: Stop old frontend processes
echo -e "${YELLOW}Step 2: Stopping old frontend processes...${NC}"
kill_port 3000
pkill -f "next dev" || true
sleep 2

echo ""
echo -e "${GREEN}✅ All old processes stopped${NC}"
echo ""

# Step 3: Start backend
echo -e "${YELLOW}Step 3: Starting Phase-03 Backend...${NC}"
cd "$SCRIPT_DIR/backend"

# Activate virtual environment and start backend
if [ -d "venv" ]; then
    source venv/bin/activate

    # Start backend in background
    nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    BACKEND_PID=$!

    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
    echo "   Logs: $SCRIPT_DIR/backend/backend.log"
    echo "   URL: http://localhost:8000"
else
    echo -e "${RED}❌ Virtual environment not found in backend/venv${NC}"
    echo "   Please run: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Wait for backend to start
echo "   Waiting for backend to initialize..."
sleep 5

# Step 4: Start frontend
echo ""
echo -e "${YELLOW}Step 4: Starting Phase-03 Frontend...${NC}"
cd "$SCRIPT_DIR/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
fi

# Start frontend in background
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "   Logs: $SCRIPT_DIR/frontend/frontend.log"
echo "   URL: http://localhost:3000"

# Step 5: Summary
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Backend:"
echo "  • URL: http://localhost:8000"
echo "  • Docs: http://localhost:8000/docs"
echo "  • Logs: tail -f $SCRIPT_DIR/backend/backend.log"
echo ""
echo "Frontend:"
echo "  • URL: http://localhost:3000"
echo "  • Logs: tail -f $SCRIPT_DIR/frontend/frontend.log"
echo ""
echo "To stop services:"
echo "  • Backend: kill $BACKEND_PID"
echo "  • Frontend: kill $FRONTEND_PID"
echo ""
echo -e "${YELLOW}Fixes Applied:${NC}"
echo "  ✓ API timeout increased to 60 seconds"
echo "  ✓ Hydration warnings suppressed"
echo ""
echo "Opening application in 3 seconds..."
sleep 3

# Try to open browser (works on WSL with Windows browser)
if command -v explorer.exe &> /dev/null; then
    explorer.exe "http://localhost:3000" 2>/dev/null || true
elif command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:3000" 2>/dev/null || true
fi

echo -e "${GREEN}Happy coding! 🚀${NC}"
