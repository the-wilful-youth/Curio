#!/bin/bash
# Fast local development script for Curio (Runs FastAPI backend & Next.js frontend)

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BACKEND_DIR="$DIR/backend"
FRONTEND_DIR="$DIR/frontend"

echo "✨ Starting Curio Development Environment..."

# Clean up background jobs on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Curio services..."
    kill $(jobs -p) 2>/dev/null || true
    echo "👋 Goodbye!"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# Start Backend
echo "🚀 Launching FastAPI Backend on http://127.0.0.1:8000 ..."
cd "$BACKEND_DIR"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# Start Frontend
echo "💻 Launching Next.js Frontend on http://localhost:3000 ..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo " Curio is live!"
echo " • Web UI:       http://localhost:3000"
echo " • Backend API:  http://127.0.0.1:8000"
echo " • API Docs:     http://127.0.0.1:8000/docs"
echo " Press [Ctrl+C] to stop both servers."
echo "=========================================="
echo ""

wait
