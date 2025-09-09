#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Load .env file FIRST before any other imports
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# NOW import the rest
from server.mcp_server import MCPServer

server = MCPServer()
app = server.app

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 8080))
    app.run(host='0.0.0.0', port=port)