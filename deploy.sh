#!/bin/bash
echo "Deploying AyaSentinel MCP Server..."

# Build and test
pip install -r requirements.txt
pytest tests/ -v

# Create Procfile for Heroku/Render
echo "web: gunicorn server.app:main --bind 0.0.0.0:$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

echo "Deployment ready! Push to Heroku or Render"
