#!/bin/bash

# Create a timestamp in UTC+6
timestamp=$(TZ=Asia/Dhaka date +"%Y-%m-%d_%H-%M-%S")

# Set filename
log_file="docker_logs_$timestamp.txt"

# Create and append logs to the file
echo "📦 Docker Logs as of $timestamp (UTC+6)" > "$log_file"

# Get list of running container IDs
containers=$(docker ps -q)

if [ -z "$containers" ]; then
    echo "❌ No running Docker containers found." >> "$log_file"
else
    for container in $containers; do
        name=$(docker inspect --format='{{.Name}}' "$container" | sed 's/^\/\(.*\)/\1/')
        echo -e "\n==============================" >> "$log_file"
        echo "🆔 Container: $name" >> "$log_file"
        echo "==============================" >> "$log_file"
        docker logs "$container" >> "$log_file" 2>&1
    done
fi

echo "✅ Logs saved to: $log_file"
