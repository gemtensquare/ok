#!/bin/bash

# Set up paths
folder_name=$(date +"%d_%B_%Y")
log_dir="./logs/server_logs/$folder_name"
mkdir -p "$log_dir"

# Timestamp file to remember last log read time
timestamp_file="./logs/last_log_time.txt"

# If the file exists, read from it; else, use current time
if [ -f "$timestamp_file" ]; then
    last_time=$(cat "$timestamp_file")
else
    last_time=$(date --iso-8601=seconds --date="4 hour ago")
fi

# Store the current time for next run
new_time=$(date --iso-8601=seconds)
echo "$new_time" > "$timestamp_file"

# Count files and prepare log file
file_count=$(find "$log_dir" -maxdepth 1 -type f -name "*.txt" | wc -l)
file_number=$((file_count + 1))
curtime=$(date +"%d_%B_%Y - %I_%M_%S_%p")
log_file="$log_dir/${file_number}. ${curtime}.txt"

# Get container ID
container_id=$(docker ps --filter "name=server" --format "{{.ID}}")

if [ -z "$container_id" ]; then
    echo "❌ No container found with 'server' in the name." > "$log_file"
else
    container_name=$(docker inspect --format='{{.Name}}' "$container_id" | sed 's/^\/\(.*\)/\1/')
    echo "🕒 New logs for: $container_name since -> $curtime (UTC+6)" > "$log_file"
    echo "===========================================================================" >> "$log_file"
    docker logs --since "$last_time" "$container_id" >> "$log_file" 2>&1
    echo "✅ New logs saved to: $log_file"
fi
