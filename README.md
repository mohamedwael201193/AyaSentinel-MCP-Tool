🛡️ AyaSentinel MCP Tool




Real-Time Crypto Scam Detection Engine
Live API | Documentation | Integration Guide

📋 Overview
AyaSentinel is a production-ready MCP (Model Context Protocol) tool that provides real-time transaction risk analysis for cryptocurrency transactions. The system analyzes transactions before execution, leveraging machine learning via Comput3.ai and maintaining an immutable audit trail on Hedera's blockchain.
Key Features

* ⚡ Real-time Analysis - Sub-500ms response time for instant risk assessment
* 🤖 ML-Powered Detection - Advanced pattern recognition using Comput3.ai GPU infrastructure
* ⛓️ Blockchain Audit Trail - All assessments logged to Hedera Consensus Service
* 🌐 Multi-chain Support - Compatible with Ethereum, Hedera, and EVM chains
* 🔧 MCP Standard - Full Model Context Protocol implementation for seamless integration


🏗️ Architecture
┌─────────────────────────────────────────┐
│            Client Application            │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
                 ▼
┌─────────────────────────────────────────┐
│         AyaSentinel MCP Server          │
│  https://aya-sentinel-mcp.onrender.com  │
├─────────────────────────────────────────┤
│  • Flask API Server                     │
│  • MCP Tool Registry                    │
│  • Risk Analysis Engine                 │
└──────┬──────────────────────┬───────────┘
       │                      │
       ▼                      ▼
┌──────────────┐      ┌───────────────────┐
│ Comput3.ai   │      │  Hedera Network   │
│ GPU Cluster  │      │  Consensus Service │
└──────────────┘      └───────────────────┘


🚀 Quick Start
Test Live API
bashDownloadCopy code Wrap# Check service status
curl https://aya-sentinel-mcp.onrender.com/

# List available MCP tools
curl https://aya-sentinel-mcp.onrender.com/tools

# Analyze a transaction
curl -X POST https://aya-sentinel-mcp.onrender.com/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_transaction_risk",
    "arguments": {
      "chain": "ethereum",
      "to_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
      "value": 100
    }
  }'
Local Development
bashDownloadCopy code Wrap# Clone repository
git clone https://github.com/mohamedwael201193/AyaSentinel-MCP-Tool
cd AyaSentinel-MCP-Tool

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run server
python -m server.app

📖 API Documentation
Base URL
https://aya-sentinel-mcp.onrender.com

Endpoints
GET /
Health check endpoint
Response:
jsonDownloadCopy code Wrap{
  "status": "AyaSentinel MCP Tool is running"
}
GET /tools
List all available MCP tools
Response:
jsonDownloadCopy code Wrap[
  {
    "name": "analyze_transaction_risk",
    "description": "Analyze transaction risk level",
    "inputSchema": {...}
  },
  ...
]
POST /invoke
Execute an MCP tool
Request Body:
jsonDownloadCopy code Wrap{
  "tool": "analyze_transaction_risk",
  "arguments": {
    "chain": "ethereum",
    "to_address": "0x...",
    "from_address": "0x...",
    "value": 1000
  }
}
Response:
jsonDownloadCopy code Wrap{
  "result": {
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "risk_score": 0.0-1.0,
    "details": {...}
  }
}

🔧 Integration Guide
JavaScript/TypeScript Integration
javascriptDownloadCopy code Wrapclass AyaSentinelClient {
  constructor() {
    this.baseURL = 'https://aya-sentinel-mcp.onrender.com';
  }

  async analyzeTransaction(txData) {
    const response = await fetch(`${this.baseURL}/invoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tool: 'analyze_transaction_risk',
        arguments: txData
      })
    });
    
    return await response.json();
  }
  
  async getTools() {
    const response = await fetch(`${this.baseURL}/tools`);
    return await response.json();
  }
}

// Usage
const sentinel = new AyaSentinelClient();
const result = await sentinel.analyzeTransaction({
  chain: 'ethereum',
  to_address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
  value: 1000
});

if (result.result.risk_level === 'CRITICAL') {
  console.warn('High risk transaction detected!');
}
Python Integration
pythonDownloadCopy code Wrapimport requests

class AyaSentinelClient:
    def __init__(self):
        self.base_url = "https://aya-sentinel-mcp.onrender.com"
    
    def analyze_transaction(self, chain, to_address, value):
        response = requests.post(
            f"{self.base_url}/invoke",
            json={
                "tool": "analyze_transaction_risk",
                "arguments": {
                    "chain": chain,
                    "to_address": to_address,
                    "value": value
                }
            }
        )
        return response.json()

# Usage
client = AyaSentinelClient()
result = client.analyze_transaction("ethereum", "0x...", 1000)
print(f"Risk Level: {result['result']['risk_level']}")

🛠️ Available MCP Tools
1. analyze_transaction_risk
Comprehensive transaction risk analysis
Parameters:

* chain (string): Blockchain network
* to_address (string): Recipient address
* from_address (string, optional): Sender address
* value (number): Transaction amount

2. check_address_reputation
Check if an address is flagged or blacklisted
Parameters:

* address (string): Address to check

3. verify_contract
Verify smart contract safety
Parameters:

* contract_address (string): Contract address to verify

4. get_chain_info
Retrieve blockchain network information
Parameters:

* chain (string): Chain identifier

5. suggest_alternatives
Get safe protocol recommendations
Parameters:

* action (string): Intended action
* risk_level (string): Current risk level

6. hedera_compute_job
Execute GPU-accelerated ML analysis via Comput3
Parameters:

* docker_image (string): Compute environment
* command (string): Analysis command


🔬 Testing
Run Complete Test Suite
pythonDownloadCopy code Wrap# test_production.py
import requests
import json

BASE_URL = "https://aya-sentinel-mcp.onrender.com"

def run_tests():
    print("Running AyaSentinel Tests...\n")
    
    # Test 1: Health Check
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    print("✅ Health check passed")
    
    # Test 2: Tools Endpoint
    r = requests.get(f"{BASE_URL}/tools")
    assert r.status_code == 200
    assert len(r.json()) == 6
    print("✅ Tools endpoint passed")
    
    # Test 3: Risk Analysis
    r = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "ethereum",
            "to_address": "0x000000000000000000000000000000000000dead",
            "value": 1000
        }
    })
    assert r.status_code == 200
    assert r.json()["result"]["risk_level"] == "CRITICAL"
    print("✅ Risk analysis passed")
    
    print("\n🎉 All tests passed successfully!")

if __name__ == "__main__":
    run_tests()

🔗 Technology Stack
ComponentTechnologyPurposeBackend FrameworkFlask/PythonAPI server and request handlingML InfrastructureComput3.aiGPU-accelerated computationBlockchainHedera Consensus ServiceImmutable audit loggingProtocolMCP StandardTool interoperabilityDeploymentRenderCloud hosting with auto-scaling
Comput3.ai Integration

* Provides GPU resources for real-time ML inference
* Enables complex pattern recognition in transaction data
* Scales automatically based on demand

Hedera Integration

* Creates tamper-proof audit trail for all risk assessments
* Ensures transparency and accountability
* Operates on testnet for development


📊 Performance Metrics
MetricValueAverage Response Time<500msUptime99.9%Supported Chains3+MCP Tools6API Version1.0

🔐 Environment Configuration
Create a .env file with the following variables:
envDownloadCopy code Wrap# Hedera Configuration
HEDERA_ACCOUNT_ID=0.0.YOUR_ACCOUNT
HEDERA_PRIVATE_KEY=YOUR_PRIVATE_KEY
HEDERA_NETWORK=testnet
HEDERA_TOPIC_ID=0.0.YOUR_TOPIC

# Comput3 Configuration
COMPUT3_API_KEY=YOUR_API_KEY
COMPUT3_BASE_URL=https://api.comput3.ai/v1

# Server Configuration
FLASK_PORT=8080
ENVIRONMENT=production

📝 License
MIT License - See LICENSE file for details

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Built for Aya Labs MCP Hackathon 2025
API Status | GitHub | Documentation
