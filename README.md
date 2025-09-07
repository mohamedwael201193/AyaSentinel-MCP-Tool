# AyaSentinel - AI-Powered Scam Detection MCP Tool

## Overview

AyaSentinel is an MCP (Model Context Protocol) server that provides AI-powered scam detection for cryptocurrency transactions. It integrates with Hedera blockchain for transparent logging and Comput3.ai for ML-based risk analysis.

## Features

- Real-time transaction risk analysis
- Smart contract verification
- Address reputation checking
- ML-powered scam detection using Comput3.ai
- Transparent logging on Hedera Consensus Service
- Multi-chain support (Ethereum, BSC, Polygon, Hedera, etc.)

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/aya-sentinel-mcp.git
cd aya-sentinel-mcp
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Add your Hedera testnet credentials
3. Add your Comput3.ai API key

### Running Locally

```bash
python server/app.py
```

Server will start on http://localhost:8080

### Testing

```bash
pytest tests/ -v
```

## API Endpoints

### GET /tools

Returns list of available MCP tools

### POST /invoke

Execute a specific tool

```json
{
  "tool": "analyze_transaction_risk",
  "arguments": {
    "chain": "ethereum",
    "to_address": "0x...",
    "value": 100
  }
}
```

## Deployment

See deployment section for Render/Heroku instructions.

## Architecture

- Flask-based MCP server
- Hedera HCS for immutable logging
- Comput3.ai for GPU-accelerated ML
- Multi-chain transaction analysis

## Demo Video

[Link to demo video]

## License

MIT
