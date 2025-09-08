import os
import json
import requests
import random
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger("AyaSentinel.Compute3Client")

class Compute3Client:
    def __init__(self):
        self.api_key = os.getenv('COMPUT3_API_KEY')
        self.base_url = os.getenv('COMPUT3_BASE_URL', 'https://api.comput3.ai/v1')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def run_scam_detection_model(self, transaction_data: Dict) -> Dict:
        """Run ML model for scam detection on Compute3"""
        try:
            # Extract features
            features = self.extract_features(transaction_data)
            
            # Check for known scam addresses first
            to_address = transaction_data.get('to_address', '').lower()
            known_scams = [
                '0x000000000000000000000000000000000000dead',
                '0x1234567890abcdef1234567890abcdef12345678'
            ]
            
            if to_address in known_scams:
                return {
                    "success": True,
                    "risk_score": 0.95,
                    "risk_level": "CRITICAL",
                    "factors": ["Known scam address", "Blacklisted", "High risk pattern"],
                    "compute_time_ms": 50,
                    "model_version": "2.0.1",
                    "compute_provider": "Comput3.ai",
                    "alert": "⚠️ KNOWN SCAM ADDRESS DETECTED"
                }
            
            # Simulate Compute3 API call (with fallback)
            try:
                if self.api_key and self.api_key != 'your_api_key_here':
                    payload = {
                        "model": "scam_detector_v2",
                        "task": "classification",
                        "data": {
                            "features": features,
                            "metadata": transaction_data
                        },
                        "compute_type": "GPU_OPTIMIZED",
                        "priority": "high"
                    }
                    
                    # For demo, simulate response
                    # In production, uncomment the actual API call
                    # response = requests.post(
                    #     f"{self.base_url}/compute",
                    #     headers=self.headers,
                    #     json=payload,
                    #     timeout=30
                    # )
                    
                    # Simulated response based on features
                    risk_score = sum(features) / len(features) if features else 0.5
                    
                    return {
                        "success": True,
                        "risk_score": risk_score,
                        "risk_level": self.calculate_risk_level(risk_score),
                        "factors": self.generate_risk_factors(risk_score, transaction_data),
                        "compute_time_ms": random.randint(100, 300),
                        "model_version": "2.0.1",
                        "compute_provider": "Comput3.ai (simulated)"
                    }
                else:
                    logger.warning("No valid API key for Comput3.ai, falling back to local risk analysis.")
                    return self.local_risk_analysis(features)
                    
            except requests.exceptions.RequestException as req_exc:
                logger.warning(f"Comput3.ai API call failed: {req_exc}. Falling back to local risk analysis.")
                return self.local_risk_analysis(features)
            except Exception as e:
                logger.warning(f"Unexpected error in Comput3.ai API call: {e}. Falling back to local risk analysis.")
                return self.local_risk_analysis(features)
                
        except Exception as e:
            logger.error(f"Error in run_scam_detection_model: {e}", exc_info=True)
            return {
                "success": False,
                "risk_score": 0.5,
                "risk_level": "UNKNOWN",
                "error": str(e),
                "compute_provider": "Local (fallback)"
            }
    
    def extract_features(self, transaction_data: Dict) -> List[float]:
        """Extract ML features from transaction data"""
        features = []
        
        # Transaction value normalized
        value = transaction_data.get('value', 0)
        features.append(min(value / 1000, 1.0))  # Normalize to 0-1
        
        # Address entropy (randomness indicator)
        to_address = transaction_data.get('to_address', '')
        features.append(self.calculate_entropy(to_address))
        
        # Chain risk factor
        chain_risks = {
            'ethereum': 0.3, 'bsc': 0.5, 'polygon': 0.2,
            'hedera': 0.1, 'arbitrum': 0.25, 'base': 0.3
        }
        chain = transaction_data.get('chain', 'ethereum').lower()
        features.append(chain_risks.get(chain, 0.5))
        
        # Contract interaction flag
        features.append(1.0 if transaction_data.get('contract_address') else 0.0)
        
        # Time-based risk (late night transactions)
        from datetime import datetime
        hour = datetime.now().hour
        features.append(1.0 if hour < 6 or hour > 22 else 0.0)
        
        return features
    
    def calculate_entropy(self, address: str) -> float:
        """Calculate address entropy (randomness)"""
        if not address:
            return 0.5
        
        # Simple entropy calculation
        char_counts = {}
        for char in address.lower():
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        length = len(address)
        for count in char_counts.values():
            if count > 0:
                prob = count / length
                import math
                entropy -= prob * math.log2(prob)
        
        # Normalize to 0-1
        return min(entropy / 4.0, 1.0)
    
    def calculate_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score < 0.3:
            return "LOW"
        elif risk_score < 0.6:
            return "MEDIUM"
        elif risk_score < 0.8:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def generate_risk_factors(self, risk_score: float, transaction_data: Dict) -> List[str]:
        """Generate risk factors based on analysis"""
        factors = []
        
        if risk_score > 0.7:
            factors.append("High risk transaction pattern")
        
        if transaction_data.get('value', 0) > 500:
            factors.append("Large transaction amount")
        
        to_address = transaction_data.get('to_address', '').lower()
        if '0000' in to_address:
            factors.append("Suspicious address pattern")
        
        chain = transaction_data.get('chain', '').lower()
        if chain in ['bsc', 'polygon']:
            factors.append(f"Higher risk chain: {chain}")
        
        if not factors:
            factors.append("No significant risk factors detected")
        
        return factors
    
    def local_risk_analysis(self, features: List[float]) -> Dict:
        """Fallback local risk analysis"""
        # Simple weighted average for demo
        weights = [0.3, 0.2, 0.2, 0.2, 0.1]
        risk_score = sum(f * w for f, w in zip(features[:len(weights)], weights))
        
        return {
            "success": True,
            "risk_score": risk_score,
            "risk_level": self.calculate_risk_level(risk_score),
            "factors": ["High value transaction"] if features[0] > 0.5 else ["Low risk profile"],
            "compute_time_ms": 50,
            "model_version": "1.0.0-local",
            "compute_provider": "Local (fallback)"
        }
    
    def run_pattern_analysis(self, addresses: List[str]) -> Dict:
        """Analyze patterns across multiple addresses"""
        try:
            # Simulated pattern analysis
            patterns = []
            
            for addr in addresses:
                if '0000' in addr.lower():
                    patterns.append("Null address pattern detected")
                if len(set(addr.lower())) < 10:
                    patterns.append("Low entropy address")
            
            return {
                "patterns": patterns if patterns else ["No suspicious patterns"],
                "clusters": len(patterns),
                "analyzed": len(addresses)
            }
            
        except Exception:
            return {"patterns": [], "clusters": 0}
