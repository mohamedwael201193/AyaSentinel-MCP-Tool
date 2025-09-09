🛡️ AyaSentinel MCP Tool





A production-ready MCP server for real-time crypto transaction risk analysis with optional on-chain logging via Hedera.

Security notice: Never commit or share private keys or API tokens. Rotate any exposed credentials immediately and update your environment variables accordingly.


🔗 Live Endpoints

* Health: https://aya-sentinel-mcp.onrender.com/
* Tools: https://aya-sentinel-mcp.onrender.com/tools
* Invoke: POST https://aya-sentinel-mcp.onrender.com/invoke
* Hedera log: POST https://aya-sentinel-mcp.onrender.com/api/scan/transaction


✨ Overview
AyaSentinel analyzes transaction metadata, address reputation, and smart contract signals to return a clear risk score and contextual details—before funds are moved. It exposes capabilities via the Model Context Protocol (MCP) for seamless integration in agentic apps such as Aya.
Key capabilities:

* Real-time risk scoring for common Web3 operations
* ML-assisted threat signals via Comput3.ai
* Hedera-based immutable audit logs (optional)
* Clean MCP interface with 6 tools


🧩 Architecture
mermaidDownloadCopy code Wrapgraph LR
    A[Aya App / Client] -->|MCP| B[AyaSentinel MCP Server]
    B --> C[Comput3.ai ML]
    B --> D[Hedera HCS (optional)]
    C --> E[Risk Score + Details]
    D --> F[Immutable Log]

🛠️ MCP Tools
Tool namePurposeMinimal inputOutput (summary)analyze_transaction_riskEnd-to-end risk analysis of a transactionchain, to_address, value (+ optional metadata)risk_level, risk_score, detailscheck_address_reputationQuick address reputation checkaddressreputation, riskverify_contractLightweight contract safety checkcontract_addressverified, risk, reasonget_chain_infoBasic chain/network infochainname, network, metadatasuggest_alternativesSafer protocol suggestionsoriginal_action, risk_levelalternatives[], messagehedera_compute_jobOffload/trigger ML compute via Comput3docker_image, commandjob metadata, status
Discover tools and schemas:
bashDownloadCopy code Wrapcurl https://aya-sentinel-mcp.onrender.com/tools

🔬 Instant Tests

* Health

bashDownloadCopy code Wrapcurl https://aya-sentinel-mcp.onrender.com/
# → {"status":"AyaSentinel MCP Tool is running"}

* Known scam detection

bashDownloadCopy code Wrapcurl -X POST https://aya-sentinel-mcp.onrender.com/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "analyze_transaction_risk",
    "arguments": {
      "chain": "ethereum",
      "to_address": "0x000000000000000000000000000000000000dead",
      "value": 1000
    }
  }'
# → risk_level: "CRITICAL"

* Hedera submission endpoint (logs the analysis hash)

bashDownloadCopy code Wrapcurl -X POST https://aya-sentinel-mcp.onrender.com/api/scan/transaction \
  -H "Content-Type: application/json" \
  -d '{"data": "some transaction data"}'
Full production test script:
bashDownloadCopy code Wrappython test_production.py
Optional comprehensive checks:
bashDownloadCopy code Wrappython test_complete.py

🤖 Aya App Integration
AyaSentinel implements the MCP interface while keeping the HTTP surface minimal. Example client-side use:
javascriptDownloadCopy code Wrap// aya-app-integration.js (example)
const AyaSentinel = {
  endpoint: 'https://aya-sentinel-mcp.onrender.com',

  async analyze(txData) {
    const res = await fetch(`${this.endpoint}/invoke`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        tool: 'analyze_transaction_risk',
        arguments: txData
      })
    });
    const data = await res.json();
    return data.result;
  }
};

// Usage:
(async () => {
  const result = await AyaSentinel.analyze({
    chain: 'ethereum',
    to_address: '0x000000000000000000000000000000000000dead',
    value: 1000
  });
  console.log(result);
})();

⚙️ Local Development

1. Install

bashDownloadCopy code Wrappip install -r requirements.txt

1. Configure environment

bashDownloadCopy code Wrapcp .env.example .env
# edit .env with your values (never commit secrets)

1. Run

bashDownloadCopy code Wrappython -m server.app
# or
gunicorn -b 0.0.0.0:8080 server.app:app

🧾 Environment Variables
Place these in your .env (not committed) or in your deployment environment.
iniDownloadCopy code Wrap# Core
FLASK_PORT=8080
ENVIRONMENT=production

# Comput3.ai
COMPUT3_API_KEY=your_comput3_api_key
COMPUT3_BASE_URL=https://api.comput3.ai/v1

# Hedera (for on-chain logging)
HEDERA_NETWORK=testnet
HEDERA_ACCOUNT_ID=0.0.xxxxxxx
HEDERA_PRIVATE_KEY=302e020100300506032b657004220420...   # never share
HEDERA_TOPIC_ID=0.0.yyyyyy

# Optional: HCS Relay URL if using a relay service
HCS_RELAY_URL=https://your-relay.example.com
HCS_RELAY_TOKEN=long_random_token
Notes:

* If HCS_RELAY_URL is set, AyaSentinel posts messages to that relay; otherwise it uses a safe local mock that writes structured logs.
* To view on-chain messages, you must use a valid Topic ID on the correct network and submit via a real SDK/relay.


⛓️ Hedera Integration
AyaSentinel supports Hedera Consensus Service (HCS) logging in two modes:

1. Development (default)


* Uses a local mock client (no Java/JNI).
* Writes Hedera-compatible log entries to a file and returns structured responses.


1. Production (on-chain)


* Submit messages to an HCS relay (or your own service) that uses the official Hedera SDK to post to your Topic ID.
* Configure:

HCS_RELAY_URL and HCS_RELAY_TOKEN
HEDERA_TOPIC_ID (testnet or mainnet)


* Verify messages on Hashscan:

Testnet: https://hashscan.io/testnet/topic/<YOUR_TOPIC_ID>
Mainnet: https://hashscan.io/mainnet/topic/<YOUR_TOPIC_ID>



Creating a Topic:

* Use Hedera Portal (recommended) to generate keys and create a topic on testnet or mainnet.
* Store keys securely; rotate if exposed.


🧠 Comput3.ai Integration

* Purpose: ML-assisted risk scoring and anomaly signals
* Configuration: COMPUT3_API_KEY and COMPUT3_BASE_URL
* Code path: server/comput3_client.py (invoked inside analyze flows)

Example request (via MCP invoke):
jsonDownloadCopy code Wrap{
  "tool": "hedera_compute_job",
  "arguments": {
    "docker_image": "python:3.11",
    "command": "python -c \"print('hello')\""
  }
}

🧪 API Reference

* 
GET /

Returns service status.


* 
GET /tools

Lists all MCP tools with their schemas.


* 
POST /invoke

Executes a tool by name with arguments.
Body:
jsonDownloadCopy code Wrap{
  "tool": "analyze_transaction_risk",
  "arguments": { "chain":"ethereum", "to_address":"...", "value": 10 }
}



* 
POST /api/scan/transaction

Accepts arbitrary JSON, derives a content hash, and logs it through the Hedera client (mock or relay).




📦 Deployment (Render example)

* Build: pip install -r requirements.txt
* Start: gunicorn -b 0.0.0.0:8080 server.app:app
* Set environment variables in the Render dashboard.
* Optional: deploy an HCS Relay (Node/JS) and set HCS_RELAY_URL/TOKEN.


📁 Repository

* Source: https://github.com/mohamedwael201193/AyaSentinel-MCP-Tool
* Live API: https://aya-sentinel-mcp.onrender.com


📄 License
MIT — see LICENSE.

If you need a minimal .env.example for the repo, use:
iniDownloadCopy code Wrap# .env.example
FLASK_PORT=8080
ENVIRONMENT=production

COMPUT3_API_KEY=
COMPUT3_BASE_URL=https://api.comput3.ai/v1

HEDERA_NETWORK=testnet
HEDERA_ACCOUNT_ID=
HEDERA_PRIVATE_KEY=
HEDERA_TOPIC_ID=

HCS_RELAY_URL=
HCS_RELAY_TOKEN=
