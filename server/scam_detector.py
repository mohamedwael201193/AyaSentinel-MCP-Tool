import logging
from typing import Dict, Any
from .hedera_client import HederaClient
from .compute3_client import Compute3Client

KNOWN_SCAM_ADDRESSES = [
    '0x000000000000000000000000000000000000dead',
    '0x1234567890abcdef1234567890abcdef12345678',
]
SAFE_PROTOCOLS = ['uniswap', 'aave', 'compound', 'curve', 'saucerswap', 'hashport']

class ScamDetector:
    def __init__(self):
        self.hedera = HederaClient()
        self.compute3 = Compute3Client()

    def analyze_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        result = {'risk_level': 'UNKNOWN', 'risk_score': 0.0, 'details': {}}
        try:
            if tx.get('to_address', '').lower() in KNOWN_SCAM_ADDRESSES:
                result['risk_level'] = 'CRITICAL'
                result['risk_score'] = 1.0
                result['details']['reason'] = 'Known scam address'
            else:
                ml_result = self.compute3.run_scam_detection_model(tx)
                score = ml_result.get('risk_score', 0.5)
                result['risk_score'] = score
                if score > 0.8:
                    result['risk_level'] = 'HIGH'
                elif score > 0.5:
                    result['risk_level'] = 'MEDIUM'
                else:
                    result['risk_level'] = 'LOW'
                result['details'].update(ml_result)
            
            self.hedera.log_risk_analysis({**tx, **result})
            
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
