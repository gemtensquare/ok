#!/bin/bash


echo "🔍 Hitting /api/news/scrape/..."
for i in {1..2}; do
  if curl --max-time 300 -sSf http://127.0.0.1:8000/api/news/scrape/; then
    echo -e "\n✅ Scraping triggered successfully!"
    # if curl -sSf http://127.0.0.1:8000/api/redis/clear/; then
    #   echo -e "\n✅ Redis cache cleared successfully!"
    #   exit 0
    exit 0
    # fi
  else
    echo "⚠️ Attempt $i: Scrape endpoint not responding or took too long. Retrying in 5s..."
    sleep 5
  fi
done

echo "❌ Scrape endpoint failed after multiple attempts."
exit 0
