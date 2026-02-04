#!/bin/bash

# OctoFit Tracker - Start All Services Script
echo "🚀 Starting OctoFit Tracker Services..."
echo "========================================"

# Navigate to the project root
cd /workspaces/flai-workshop-github-copilot-800-jjhorta

# Start Django Backend
echo ""
echo "📦 Starting Django Backend Server on port 8000..."
cd octofit-tracker/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!
echo "✅ Django Backend started (PID: $DJANGO_PID)"
cd ../..

# Wait a moment for Django to start
sleep 2

# Start React Frontend
echo ""
echo "⚛️  Starting React Frontend Server on port 3000..."
cd octofit-tracker/frontend
npm start > /tmp/react.log 2>&1 &
REACT_PID=$!
echo "✅ React Frontend started (PID: $REACT_PID)"
cd ../..

echo ""
echo "========================================"
echo "✨ All services are starting up!"
echo ""
echo "📍 Backend API:  https://$CODESPACE_NAME-8000.app.github.dev"
echo "📍 Frontend App: https://$CODESPACE_NAME-3000.app.github.dev"
echo ""
echo "📊 View logs:"
echo "   Backend:  tail -f /tmp/django.log"
echo "   Frontend: tail -f /tmp/react.log"
echo ""
echo "🛑 To stop services:"
echo "   kill $DJANGO_PID $REACT_PID"
echo ""
echo "Or use: ./stop-services.sh"
echo "========================================"

# Save PIDs to file for easy stopping
echo "$DJANGO_PID $REACT_PID" > /tmp/octofit-pids.txt
