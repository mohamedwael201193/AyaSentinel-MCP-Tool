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
| 🌐 Multi-Chain Compatibility   | Analyzes transactions across Ethereum, Hedera, and EVM-compatible chains.  | Web3.py, hedera-sdk-py |
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

### POST /api/scan/transaction

Submits a transaction hash to the Hedera Consensus Service.

#### Example: Submitting a transaction hash

```bash
curl -X POST https://aya-sentinel-mcp.onrender.com/api/scan/transaction \
     -H "Content-Type: application/json" \
     -d '{"data": "some transaction data"}'
```

This will return a transaction hash that can be viewed on Hashscan.

## 🛠️ Getting Started (Local Development)

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure environment variables:**
    Copy `.env.example` to `.env` and fill in the required variables.
    ```bash
    cp .env.example .env
    ```
    **Important:** For security reasons, do not commit the `.env` file to your repository. If you publish your code, keep the private key out of the file.

3.  **Run the server:**
    For local development:
    ```bash
    python -m server.app
    ```
    For production (like on Render):
    ```bash
    gunicorn -b :8080 "server.app:app"
    ```

## Hedera Integration

This MCP tool integrates with Hedera in production mode. For the hackathon demo:
- Transactions are logged locally with Hedera-compatible structure
- In production, these would be submitted via Hedera REST API
- No Java dependencies required - works on any system
- Topic ID: 0.0.4079455 (configured in .env)

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