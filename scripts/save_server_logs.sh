#!/bin/bash

# Set timezone to Asia/Dhaka
# export TZ=Asia/Dhaka

# Create directory with today's date
folder_name=$(date +"%d_%B_%Y")
mkdir -p "./logs/server_logs/$folder_name"

# Generate timestamp for the file
curtime=$(date +"%d_%B_%Y - %I_%M_%S_%p")
log_file="./logs/server_logs/$folder_name/$curtime.txt"

# Find the container with 'server' in the name
container_id=$(docker ps --filter "name=server" --format "{{.ID}}")

if [ -z "$container_id" ]; then
    echo "❌ No container found with 'server' in the name." > "$log_file"
else
    container_name=$(docker inspect --format='{{.Name}}' "$container_id" | sed 's/^\/\(.*\)/\1/')
    echo "🕒 Logs for container: $container_name at $curtime (UTC+6)" > "$log_file"
    echo "==============================================" >> "$log_file"
    docker logs "$container_id" >> "$log_file" 2>&1
    echo "✅ Logs saved to: $log_file"
fi
