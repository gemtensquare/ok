#!/bin/bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Starting Docker containers in detached mode...${NC}"
docker compose up -d

echo -e "${YELLOW}⏳ Waiting for services to be up and running...${NC}"
sleep 15

echo -e "${BLUE}🔍 ==================================================================${NC}"
echo -e "${GREEN}🔍 Checking News API endpoint...${NC}"
sh ./scripts/check_news_endpoint.sh

echo -e "${BLUE}🔍 ==================================================================${NC}"
echo -e "${GREEN}📰 Scraping news articles...${NC}"
sh ./scripts/scrape_news.sh

echo -e "${YELLOW}⏳ Waiting for data to be processed...${NC}"
sleep 15

echo -e "${BLUE}🔍 ==================================================================${NC}"
echo -e "${GREEN}✅ Final check on scraped news list...${NC}"
sh ./scripts/final_check_news_list.sh

echo -e "${YELLOW}⏳ Giving it a moment to stabilize...${NC}"
sleep 5

echo -e "${BLUE}🔍 ==================================================================${NC}"
echo -e "${GREEN}🔍 Backing up the GemtenAi database...${NC}"
sh ./scripts/backup_GemtenAi_db.sh

echo -e "${BLUE}🔚 ==================================================================${NC}"
echo -e "${GREEN}✅ All tasks completed successfully.${NC}"
 NOW="$(date '+%d %B %Y - %I:%M %p')"
echo "Backup database and Push update at $NOW" >> logs/auto_backup_and_push_log.txt
