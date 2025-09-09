# server/mcp_server.py

import os
import logging
from flask import Flask, jsonify, request
from .scam_detector import ScamDetector
from .compute3_client import Comput3Client
from .hedera_service import log_analysis_to_hcs

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class MCPServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.scam_detector = ScamDetector()
        # Initialize the client with the API key from environment variables
        self.comput3_client = Comput3Client(os.getenv('COMPUT3_API_KEY'))
        self._register_routes()

    def _register_routes(self):
        self.app.route("/", methods=['GET'])(self.health_check)
        self.app.route("/tools", methods=['GET'])(self.list_tools)
        self.app.route("/invoke", methods=['POST'])(self.invoke_tool)

    def health_check(self):
        return jsonify({"status": "AyaSentinel MCP Tool is running"}), 200

    def list_tools(self):
        # Tool definitions remain the same as you provided
        tools = [
            {
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
            },
            # Add other tools here if you have them (check_address_reputation, etc.)
        ]
        return jsonify(tools)

    def invoke_tool(self):
        data = request.get_json()
        if not data or "tool" not in data:
            return jsonify({"error": "Invalid request, 'tool' is required"}), 400

        tool_name = data.get("tool")
        arguments = data.get("arguments", {})

        try:
            analysis_result = None
            if tool_name == "analyze_transaction_risk":
                # This now calls the REAL Comput3.ai client
                analysis_result = self.comput3_client.analyze_transaction(arguments)
            # Add other tool logic here if needed
            # elif tool_name == "check_address_reputation":
            #     analysis_result = self.scam_detector.check_address(arguments.get('address'))
            else:
                return jsonify({"error": f"Tool '{tool_name}' not found"}), 404

            if not analysis_result or analysis_result.get("error"):
                 # If the analysis failed, return its error message directly
                return jsonify({"error": "Analysis failed", "details": analysis_result}), 500

            # Log the successful analysis to Hedera HCS
            hedera_tx_id = log_analysis_to_hcs({
                "tool_invoked": tool_name,
                "tool_arguments": arguments,
                "analysis_result": analysis_result
            })

            # Return the final, combined response
            final_response = {
                "result": analysis_result,
                "hedera_transaction_id": hedera_tx_id or "Failed to log to Hedera"
            }
            return jsonify(final_response)

        except Exception as e:
            logging.error(f"Critical error in invoke_tool: {e}", exc_info=True)
            return jsonify({"error": "An unexpected server error occurred."}), 500