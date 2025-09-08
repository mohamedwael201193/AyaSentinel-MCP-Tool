
# AyaSentinel: Real-Time Crypto Transaction Analysis Engine

A high-performance, production-ready MCP server for real-time risk analysis.

**Live API Endpoint → [https://aya-sentinel-mcp.onrender.com/tools](https://aya-sentinel-mcp.onrender.com/tools)**

</div>

AyaSentinel is a critical security layer for the Web3 ecosystem. In an environment where financial losses from scams and fraud are a major concern, our engine provides instant, actionable intelligence. By analyzing transaction metadata, address reputation, and smart contract interactions, AyaSentinel generates a risk score before a user commits to a potentially irreversible action.

By leveraging machine learning, decentralized logging, and a scalable architecture, AyaSentinel provides a robust solution for integrating advanced security intelligence into wallets, DApps, and other Web3 services.

## 核心機能 (Core Features)

| Feature                        | Description                                                                | Technology          |
| ------------------------------ | -------------------------------------------------------------------------- | ------------------- |
| ⚡ Real-Time Risk Scoring      | Delivers a risk assessment in < 500ms, enabling seamless integration.      | Flask, Gunicorn     |
| 🧠 ML-Powered Threat Detection | Utilizes Comput3.ai to identify sophisticated threats and patterns.        | Comput3.ai          |
| ⛓️ Immutable Audit Trail       | Records every analysis on Hedera Consensus Service (HCS) for transparency. | Hedera HCS          |
| 🌐 Multi-Chain Compatibility   | Analyzes transactions across Ethereum, Hedera, and EVM-compatible chains.  | Web3.py, Hedera SDK |
| 🤖 Standardized MCP Interface  | Adheres to Model Context Protocol for easy AI agent integration.           | MCP Standard        |

## 🏛️ Technical Architecture

AyaSentinel is built on a modern, scalable stack chosen for performance, reliability, and decentralization.

- **Application Framework:** Flask serves as a lightweight and robust Python web server.
- **AI/ML Integration:** The system follows the Model Context Protocol (MCP) to expose its capabilities as standardized "tools".
- **GPU-Accelerated Compute:** Comput3.ai provides the GPU resources necessary for deep transaction analysis without compromising speed.
- **Decentralized Ledger:** Hedera HCS is integrated for immutable logging of all risk assessments.
- **Deployment & Hosting:** The application is deployed on Render with continuous integration from the main branch.

## 🚀 API Endpoints & Usage

The API is live and can be tested directly.

### GET /tools

Retrieves a list of all available analysis tools and their required input schemas.

```bash
curl https://aya-sentinel-mcp.onrender.com/tools
```

### POST /invoke

Executes a specific tool to perform an analysis.

#### Example: Analyzing a Known Scam Address

```bash
curl -X POST https://aya-sentinel-mcp.onrender.com/invoke \
     -H "Content-Type: application/json" \
     -d '{
         "tool": "analyze_transaction_risk",
         "arguments": {
           "chain": "ethereum",
           "to_address": "0x000000000000000000000000000000000000dead",
           "value": 1000
         }
       }'
```

<details>
<summary>Click to see Expected Response</summary>

```json
{
  "result": {
    "risk_level": "CRITICAL",
    "risk_score": 0.95,
    "issues": ["Address is on a known scam list."],
    "recommendation": "Do not proceed with this transaction. The recipient address is associated with known fraudulent activity."
  }
}
```

</details>

## 🛠️ Getting Started (Local Development)

**Clone the Repository:**

```bash
git clone https://github.com/mohamedwael201193/AyaSentinel-MCP-Tool.git
cd AyaSentinel-MCP-Tool
```

**Set Up a Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate    # On Windows
```

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

**Configure Environment Variables:**

```bash
cp .env.example .env
# Now, edit the .env file with your API keys
```

**Run the Server:**

```bash
python -m server.app
```

## 🔬 Production API Verification

To confirm that the live, deployed service on Render is fully operational and bug-free, run the `final_test.py` script included in this repository. This end-to-end test validates all critical endpoints and measures the real-world performance of the live API.

**To run the verification script:**

```bash
# Ensure all requirements are installed
python final_test.py
```

You will see a confirmation that all tests have passed successfully.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
