#!/bin/bash

# Check if PID file exists
if [ ! -f "app.pid" ]; then
    echo "No PID file found. Application may not be running."
    exit 1
fi

# Read PID from file
PID=$(cat app.pid)

# Check if process is running
if ! ps -p $PID > /dev/null 2>&1; then
    echo "Process with PID $PID is not running"
    rm app.pid
    exit 1
fi

# Kill the process
echo "Stopping application with PID $PID..."
kill $PID

# Wait a moment and check if it's still running
sleep 2
if ps -p $PID > /dev/null 2>&1; then
    echo "Process still running, force killing..."
    kill -9 $PID
    sleep 1
fi

# Check if process is really stopped
if ps -p $PID > /dev/null 2>&1; then
    echo "Failed to stop the process"
    exit 1
else
    echo "Application stopped successfully"
    rm app.pid
fi 