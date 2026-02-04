#!/bin/bash

# OctoFit Tracker - Stop All Services Script
echo "🛑 Stopping OctoFit Tracker Services..."
echo "========================================"

# Check if PID file exists
if [ -f /tmp/octofit-pids.txt ]; then
    PIDS=$(cat /tmp/octofit-pids.txt)
    echo "Stopping processes: $PIDS"
    kill $PIDS 2>/dev/null
    rm /tmp/octofit-pids.txt
    echo "✅ Services stopped"
else
    echo "⚠️  No PID file found. Attempting to find and stop processes..."
    
    # Find and kill Django processes
    pkill -f "manage.py runserver" && echo "✅ Django stopped"
    
    # Find and kill React processes
    pkill -f "react-scripts start" && echo "✅ React stopped"
fi

echo "========================================"
echo "✨ All services stopped"
