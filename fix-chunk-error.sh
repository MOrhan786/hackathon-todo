#!/bin/bash

# Fix for ChunkLoadError in Next.js
# This script clears cache and restarts the frontend cleanly

set -e

echo "🔧 Fixing Next.js ChunkLoadError..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/frontend"

# Step 1: Stop frontend
echo -e "${YELLOW}Step 1: Stopping frontend...${NC}"
pkill -f "next dev" 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ Frontend stopped${NC}"

# Step 2: Clear Next.js cache
echo ""
echo -e "${YELLOW}Step 2: Clearing Next.js cache...${NC}"
rm -rf .next
rm -rf node_modules/.cache 2>/dev/null || true
echo -e "${GREEN}✅ Cache cleared${NC}"

# Step 3: Clear TypeScript cache
echo ""
echo -e "${YELLOW}Step 3: Clearing TypeScript cache...${NC}"
rm -rf tsconfig.tsbuildinfo 2>/dev/null || true
echo -e "${GREEN}✅ TypeScript cache cleared${NC}"

# Step 4: Restart frontend
echo ""
echo -e "${YELLOW}Step 4: Starting fresh frontend build...${NC}"
npm run dev &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend starting (PID: $FRONTEND_PID)${NC}"
echo ""

# Wait for frontend to compile
echo "⏳ Waiting for Next.js to compile..."
echo "   This may take 30-60 seconds for first compile..."
sleep 5

# Check if process is still running
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Frontend restarted successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo "URL: http://localhost:3000"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Wait for compilation to complete (watch terminal)"
    echo "2. Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)"
    echo "3. Refresh the page"
    echo ""
    echo "If you still see the error:"
    echo "• Open DevTools (F12)"
    echo "• Go to Application → Clear site data"
    echo "• Hard refresh (Ctrl+Shift+R)"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
    echo "Check the output above for errors"
    exit 1
fi
