# server/scam_detector.py
import logging
from typing import Dict, Any
import json
import hashlib
import os
logger = logging.getLogger(__name__)

KNOWN_SCAM_ADDRESSES = [
    '0x000000000000000000000000000000000000dead',
    '0x1234567890abcdef1234567890abcdef12345678',
]
SAFE_PROTOCOLS = ['uniswap', 'aave', 'compound', 'curve', 'saucerswap', 'hashport']

class ScamDetector:
    def __init__(self, hedera_client, comput3_client):
        self.hedera = hedera_client
        self.compute3 = comput3_client

    def analyze_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        result = {'risk_level': 'UNKNOWN', 'risk_score': 0.0, 'details': {}}
        try:
            if tx.get('to_address', '').lower() in KNOWN_SCAM_ADDRESSES:
                result['risk_level'] = 'CRITICAL'
                result['risk_score'] = 1.0
                result['details']['reason'] = 'Known scam address'
            else:
                ml_result = self.compute3.analyze_transaction(tx)
                score = ml_result.get('risk_score', 0.5)
                result['risk_score'] = score
                if score > 0.8:
                    result['risk_level'] = 'HIGH'
                elif score > 0.5:
                    result['risk_level'] = 'MEDIUM'
                else:
                    result['risk_level'] = 'LOW'
                result['details'].update(ml_result)
            
            # Log to Hedera
            log_data = {**tx, **result}
            log_hash = hashlib.sha256(json.dumps(log_data).encode()).hexdigest()

            hedera_result = self.hedera.submit_message_to_topic(log_hash)
            if hedera_result["success"]:
                logger.info(f"Logged to Hedera: {hedera_result['transaction_id']}")
            else:
                logger.error(f"Failed to log to Hedera: {hedera_result.get('error')}")
            
        except Exception as e:
            logger.error(f"analyze_transaction error: {e}")  # Changed from logging.error
            result['risk_level'] = 'ERROR'
            result['details']['error'] = str(e)
        return result
KNOWN_SCAM_ADDRESSES = [
    '0x000000000000000000000000000000000000dead',
    '0x1234567890abcdef1234567890abcdef12345678',
]
SAFE_PROTOCOLS = ['uniswap', 'aave', 'compound', 'curve', 'saucerswap', 'hashport']

class ScamDetector:
    def __init__(self, hedera_client, comput3_client):
        self.hedera = hedera_client
        self.compute3 = comput3_client

    def analyze_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        result = {'risk_level': 'UNKNOWN', 'risk_score': 0.0, 'details': {}}
        try:
            if tx.get('to_address', '').lower() in KNOWN_SCAM_ADDRESSES:
                result['risk_level'] = 'CRITICAL'
                result['risk_score'] = 1.0
                result['details']['reason'] = 'Known scam address'
            else:
                ml_result = self.compute3.analyze_transaction(tx)
                score = ml_result.get('risk_score', 0.5)
                result['risk_score'] = score
                if score > 0.8:
                    result['risk_level'] = 'HIGH'
                elif score > 0.5:
                    result['risk_level'] = 'MEDIUM'
                else:
                    result['risk_level'] = 'LOW'
                result['details'].update(ml_result)
            
            # Log to Hedera
            log_data = {**tx, **result}
            log_hash = hashlib.sha256(json.dumps(log_data).encode()).hexdigest()

            hedera_result = self.hedera.submit_message_to_topic(log_hash)
            if hedera_result["success"]:
                logger.info(f"Logged to Hedera: {hedera_result['transaction_id']}")
            else:
                logger.error(f"Failed to log to Hedera: {hedera_result.get('error')}")
            
        except Exception as e:
            logging.error(f"analyze_transaction error: {e}")
            result['risk_level'] = 'ERROR'
            result['details']['error'] = str(e)
        return result
    
    def quick_scam_check(self, address: str) -> bool:
        return address and address.lower() in KNOWN_SCAM_ADDRESSES

    def check_address(self, address: str) -> Dict[str, Any]:
        if self.quick_scam_check(address):
            return {'reputation': 'scam', 'risk': 1.0}
        return {'reputation': 'unknown', 'risk': 0.5}

    def verify_contract(self, contract_address: str) -> Dict[str, Any]:
        if contract_address.lower() in KNOWN_SCAM_ADDRESSES:
            return {'verified': False, 'risk': 1.0, 'reason': 'Known scam contract'}
        return {'verified': True, 'risk': 0.1}

    def suggest_alternatives(self, original_action: str, risk_level: str) -> Dict[str, Any]:
        if risk_level.upper() in ['HIGH', 'CRITICAL']:
            return {'alternatives': SAFE_PROTOCOLS, 'message': 'Use trusted protocols only.'}
        return {'alternatives': [], 'message': 'No alternatives needed.'}
