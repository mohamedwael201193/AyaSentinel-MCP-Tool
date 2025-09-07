#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from server.mcp_server import MCPServer

load_dotenv()

server = MCPServer()
app = server.app  # Export Flask app for Gunicorn

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 8080))
    app.run(host='0.0.0.0', port=port)
