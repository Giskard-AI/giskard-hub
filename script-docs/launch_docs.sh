#!/bin/bash
# Simple script to launch sphinx-autobuild for the Giskard Hub documentation

echo "🚀 Launching Giskard Hub Documentation Server..."
echo "📍 Server will be available at: http://127.0.0.1:8000"
echo "📝 Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Launch sphinx-autobuild
uv run sphinx-autobuild . _build/html --port 8000 --open-browser --host 127.0.0.1
