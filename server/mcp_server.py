import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from .scam_detector import ScamDetector
from dotenv import load_dotenv
from functools import wraps
import time

load_dotenv()

def rate_limit(max_per_minute=30):
    calls = {}
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            window = int(now // 60)
            if ip not in calls:
                calls[ip] = {}
            if window not in calls[ip]:
                calls[ip] = {window: 0}
            if calls[ip][window] >= max_per_minute:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            calls[ip][window] += 1
            return f(*args, **kwargs)
        return wrapped
    return decorator

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
            },
            {
                'name': 'check_address_reputation',
                'description': 'Check if address has scam history',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'address': {'type': 'string'}
                    },
                    'required': ['address']
                }
            },
            {
                'name': 'verify_smart_contract',
                'description': 'Verify contract safety',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'contract_address': {'type': 'string'}
                    },
                    'required': ['contract_address']
                }
            },
            {
                'name': 'get_safe_alternatives',
                'description': 'Suggest safe alternatives for risky transactions',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'original_action': {'type': 'string'},
                        'risk_level': {'type': 'string'}
                    },
                    'required': ['original_action', 'risk_level']
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

        @self.app.route('/resources', methods=['GET'])
        def resources():
            return jsonify({'resources': ['transactions', 'addresses', 'contracts']})

        @self.app.route('/invoke', methods=['POST'])
        @rate_limit()
        def invoke():
            data = request.get_json(force=True)
            tool = data.get('tool')
            args = data.get('arguments', {})
            if tool == 'analyze_transaction_risk':
                result = self.detector.analyze_transaction(args)
                return jsonify({'result': result})
            elif tool == 'check_address_reputation':
                address = args.get('address')
                result = self.detector.check_address(address)
                return jsonify({'result': result})
            elif tool == 'verify_smart_contract':
                contract_address = args.get('contract_address')
                result = self.detector.verify_contract(contract_address)
                return jsonify({'result': result})
            elif tool == 'get_safe_alternatives':
                original_action = args.get('original_action')
                risk_level = args.get('risk_level')
                result = self.detector.suggest_alternatives(original_action, risk_level)
                return jsonify({'result': result})
            else:
                return jsonify({'error': 'Unknown tool'}), 400

    def run(self, host='0.0.0.0', port=8080):
        logging.info(f"Starting MCP Server on {host}:{port}")
        self.app.run(host=host, port=port)
