import os
import requests
import logging
import numpy as np
from typing import Dict, Any, List

class Compute3Client:
    def __init__(self):
        self.api_key = os.getenv('COMPUT3_API_KEY')
        self.base_url = os.getenv('COMPUT3_BASE_URL', 'https://api.comput3.ai/v1')
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def run_scam_detection_model(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/scam-detect"
            resp = requests.post(url, json=tx_data, headers=self.headers, timeout=3)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {'risk_score': 0.5, 'error': 'API error'}
        except Exception as e:
            logging.error(f"Compute3 run_scam_detection_model error: {e}")
            return self.local_risk_analysis(tx_data)

    def extract_features(self, tx_data: Dict[str, Any]) -> List[float]:
        # Simple feature extraction for demo
        features = [len(str(tx_data.get('to_address', ''))), float(tx_data.get('value', 0))]
        return features

    def calculate_entropy(self, address: str) -> float:
        # Calculate entropy of address string
        prob = [float(address.count(c)) / len(address) for c in set(address)]
        entropy = -sum([p * np.log2(p) for p in prob])
        return entropy

    def local_risk_analysis(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        # Fallback ML logic
        features = self.extract_features(tx_data)
        risk_score = min(1.0, (features[1] / 10000.0) + (1.0 - self.calculate_entropy(tx_data.get('to_address', '')) / 4.0))
        return {'risk_score': risk_score, 'source': 'local'}

    def pattern_analysis(self, addresses: list) -> Dict[str, Any]:
        # Analyze multiple addresses for patterns
        entropies = [self.calculate_entropy(addr) for addr in addresses]
        avg_entropy = float(np.mean(entropies)) if entropies else 0.0
        return {'avg_entropy': avg_entropy, 'entropies': entropies}
