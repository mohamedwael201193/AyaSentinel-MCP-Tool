# server/mcp_server.py
import os
import logging
import hashlib
import json
from flask import Flask, jsonify, request
from .scam_detector import ScamDetector
from .compute3_client import Comput3Client
from .hedera_service import hedera_client

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOOL_COMPUTE = {
    "name": "hedera_compute_job",
    "description": "Spin-up an ephemeral GPU pod on Comput3.ai and return the jobId",
    "input_schema": {
        "type": "object",
        "properties": {
            "docker_image": {"type": "string"},
            "command":      {"type": "string"}
        },
        "required": ["docker_image", "command"]
    }
}

TOOL_SCAN_DETECTION = {
    "name": "analyze_transaction_risk",
    "description": "Analyzes a blockchain transaction for potential risks like scams or fraud using an AI model.",
    "parameters": {
        "type": "object",
        "properties": {
            "chain": {"type": "string", "description": "The blockchain name (e.g., 'hedera', 'ethereum')."},
            "to_address": {"type": "string", "description": "The recipient's wallet address."},
            "from_address": {"type": "string", "description": "The sender's wallet address. Optional."},
            "value": {"type": "number", "description": "The transaction amount in native currency."},
            "data": {"type": "string", "description": "The transaction data payload. Optional."}
        },
        "required": ["chain", "to_address", "value"]
    }
}

# Placeholders for other tools
TOOL_SAFE_TRANSACTION = {"name": "safe_transaction", "description": "Placeholder for safe transaction tool"}
TOOL_ADDRESS_REPUTATION = {"name": "address_reputation", "description": "Placeholder for address reputation tool"}
TOOL_CONTENT_VERIFICATION = {"name": "content_verification", "description": "Placeholder for content verification tool"}
TOOL_SAFE_ALTERNATIVES = {"name": "safe_alternatives", "description": "Placeholder for safe alternatives tool"}


class MCPServer:
    def __init__(self):
        self.app = Flask(__name__)
        # Initialize the clients
        self.comput3_client = Comput3Client(os.getenv('COMPUT3_API_KEY'))
        # Pass clients to ScamDetector
        self.scam_detector = ScamDetector(hedera_client, self.comput3_client)
        self._register_routes()

    def _register_routes(self):
        self.app.route("/", methods=['GET'])(self.health_check)
        self.app.route("/tools", methods=['GET'])(self.list_tools)
        self.app.route("/invoke", methods=['POST'])(self.invoke_tool)
        self.app.route("/api/scan/transaction", methods=["POST"])(self.scan_transaction)

    def health_check(self):
        return jsonify({"status": "AyaSentinel MCP Tool is running"}), 200

    def list_tools(self):
        return jsonify([
            TOOL_COMPUTE,
            TOOL_SCAN_DETECTION,
            TOOL_SAFE_TRANSACTION,
            TOOL_ADDRESS_REPUTATION,
            TOOL_CONTENT_VERIFICATION,
            TOOL_SAFE_ALTERNATIVES
        ])

    def scan_transaction(self):
        data = request.get_json()
        tx_hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
        
        try:
            # Use the mock client's method
            result = hedera_client.submit_message_to_topic(tx_hash)
            
            if result["success"]:
                return jsonify({
                    "txHash": tx_hash, 
                    "status": "submitted",
                    "hedera_result": result
                })
            else:
                return jsonify({"error": result.get("error", "Unknown error")}), 500
                
        except Exception as e:
            logging.error(f"Failed to submit to Hedera: {e}")
            return jsonify({"error": str(e)}), 500
    
    def invoke_tool(self):
        data = request.get_json()
        if not data or "tool" not in data:
            return jsonify({"error": "Invalid request, 'tool' is required"}), 400

        tool_name = data.get("tool")
        arguments = data.get("arguments", {})

        try:
            result = None
            if tool_name == "hedera_compute_job":
                image = arguments.get("docker_image")
                command = arguments.get("command")
                job_id = self.comput3_client.run_compute_job(image, command)
                result = {"jobId": job_id}
            elif tool_name == "analyze_transaction_risk":
                result = self.scam_detector.analyze_transaction(arguments)
            else:
                return jsonify({"error": f"Tool '{tool_name}' not found"}), 404

            if not result or result.get("error"):
                return jsonify({"error": "Analysis failed", "details": result}), 500

            return jsonify({"result": result})

        except Exception as e:
            logging.error(f"Critical error in invoke_tool: {e}", exc_info=True)
            return jsonify({"error": "An unexpected server error occurred."}), 500
