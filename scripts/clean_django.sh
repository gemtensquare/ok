#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔍 Searching for Django migrations and Python files to delete...${NC}"

# Delete all migrations folders except __init__.py
# find . -type d -name "migrations" | while read dir; do
#   echo -e "${RED}🗑️ Deleting Python files in $dir (except __init__.py)...${NC}"
#   find "$dir" -type f -name "*.py" ! -name "__init__.py" -delete
#   find "$dir" -type f -name "*.pyc" -delete
# done

# Optionally delete all migrations folders completely (uncomment below if needed)
# echo -e "${RED}🗑️ Deleting all 'migrations' directories...${NC}"
# find . -type d -name "migrations" -exec rm -rf {} +

# Delete all .pyc files
echo -e "${RED}🧹 Deleting all .pyc files...${NC}"
find . -type f -name "*.pyc" -delete

# Delete all __pycache__ folders
echo -e "${RED}🧹 Deleting all __pycache__ directories...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} +

echo -e "${GREEN}✅ Cleanup completed!${NC}"
