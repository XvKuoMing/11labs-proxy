#!/bin/bash

# Check if already running
if [ -f "app.pid" ]; then
    PID=$(cat app.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Application is already running with PID $PID"
        exit 1
    else
        echo "Removing stale PID file"
        rm app.pid
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the application with nohup and save PID
echo "Starting main.py with uv..."
nohup uv run main.py > logs/app.log 2>&1 &
PID=$!

# Save PID to file
echo $PID > app.pid

echo "Application started with PID $PID"
echo "Logs are being written to logs/app.log"
echo "Use ./stop.sh to stop the application" 