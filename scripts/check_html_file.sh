#!/bin/bash

# Default directory is current if none provided
DIR="${1:-.}"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  echo "❌ Directory not found: $DIR"
  exit 1
fi

echo "📂 Searching for HTML files in: $DIR"
echo "--------------------------------------"

# Find and print all .html files recursively
find "$DIR" -type f -name "*.html"
