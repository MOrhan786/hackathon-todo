#!/bin/bash

# Push Phase 3 to GitHub
# Repository: https://github.com/MOrhan786/hackathon-todo

set -e

echo "🚀 Pushing Phase 3 to GitHub..."
echo ""
echo "Repository: https://github.com/MOrhan786/hackathon-todo"
echo "Branch: master"
echo "Tag: phase-3"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Not a git repository${NC}"
    exit 1
fi

# Check if tag exists
if ! git tag | grep -q "^phase-3$"; then
    echo -e "${RED}❌ Error: Tag 'phase-3' not found${NC}"
    echo "   Creating tag now..."
    git tag -a phase-3 -m "Phase 3: AI-Powered Todo Application"
    echo -e "${GREEN}✅ Tag created${NC}"
fi

# Check remote
if ! git remote | grep -q "^origin$"; then
    echo -e "${RED}❌ Error: Remote 'origin' not configured${NC}"
    echo "   Adding remote..."
    git remote add origin https://github.com/MOrhan786/hackathon-todo.git
    echo -e "${GREEN}✅ Remote added${NC}"
fi

echo -e "${YELLOW}Attempting to push to GitHub...${NC}"
echo ""
echo -e "${BLUE}If prompted for credentials:${NC}"
echo "  Username: MOrhan786"
echo "  Password: Use your GitHub Personal Access Token"
echo ""
echo -e "${BLUE}Get token at: https://github.com/settings/tokens${NC}"
echo ""

# Push master branch
echo -e "${YELLOW}Step 1: Pushing master branch...${NC}"
if git push -u origin master; then
    echo -e "${GREEN}✅ Master branch pushed successfully${NC}"
else
    echo -e "${RED}❌ Failed to push master branch${NC}"
    echo ""
    echo "Possible solutions:"
    echo "1. Make sure you're using a Personal Access Token as password"
    echo "2. Token must have 'repo' scope enabled"
    echo "3. Try: git push https://MOrhan786@github.com/MOrhan786/hackathon-todo.git master"
    echo ""
    echo "Get token: https://github.com/settings/tokens"
    exit 1
fi

echo ""

# Push tag
echo -e "${YELLOW}Step 2: Pushing phase-3 tag...${NC}"
if git push origin phase-3; then
    echo -e "${GREEN}✅ Tag pushed successfully${NC}"
else
    echo -e "${RED}❌ Failed to push tag${NC}"
    echo ""
    echo "Try manually: git push origin phase-3"
    exit 1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "View on GitHub:"
echo "  • Repository: https://github.com/MOrhan786/hackathon-todo"
echo "  • Commits: https://github.com/MOrhan786/hackathon-todo/commits/master"
echo "  • Tags: https://github.com/MOrhan786/hackathon-todo/tags"
echo "  • Phase 3 Tag: https://github.com/MOrhan786/hackathon-todo/releases/tag/phase-3"
echo ""
echo -e "${GREEN}🎉 Phase 3 is now live on GitHub!${NC}"
