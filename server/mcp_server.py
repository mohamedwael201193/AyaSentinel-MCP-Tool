import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from .scam_detector import ScamDetector
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger("AyaSentinel.MCPServer")

class MCPServer:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.detector = ScamDetector()
        self.tools = self._define_tools()
        self._register_routes()

    def _define_tools(self):
        return [
            {
                'name': 'analyze_transaction_risk',
                'description': 'Analyze transaction for scam indicators using ML',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'chain': {'type': 'string'},
                        'to_address': {'type': 'string'},
                        'from_address': {'type': 'string'},
                        'value': {'type': 'number'}
                    },
                    'required': ['chain', 'to_address', 'value']
                }
            }
        ]

    def _register_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy'})

        @self.app.route('/tools', methods=['GET'])
        def tools():
            return jsonify({'tools': self.tools})

        @self.app.route('/invoke', methods=['POST'])
        def invoke():
            data = request.get_json(force=True)
            tool = data.get('tool')
            args = data.get('arguments', {})
            logger.info(f"Invoking tool: {tool} | Arguments: {json.dumps(args)}")
            try:
                if tool == 'analyze_transaction_risk':
                    result = self.detector.analyze_transaction(args)
                    return jsonify({'result': result})
                else:
                    logger.error(f"Unknown tool requested: {tool}")
                    return jsonify({'error': 'Unknown tool'}), 400
            except Exception as e:
                logger.error(f"Error in /invoke for tool {tool}: {e}", exc_info=True)
                return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    def run(self, host='0.0.0.0', port=8080):
        logger.info(f"Starting MCP Server on {host}:{port}")
        self.app.run(host=host, port=port)
