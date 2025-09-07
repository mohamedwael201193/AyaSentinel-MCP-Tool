import requests
import json

BASE_URL = "http://localhost:8080"

def test_scam_detection():
    # Test 1: Safe transaction
    print("Testing safe transaction...")
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "hedera",
            "to_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "value": 10
        }
    })
    print(f"Safe tx result: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Known scam
    print("\nTesting known scam address...")
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "ethereum",
            "to_address": "0x000000000000000000000000000000000000dead",
            "value": 1000
        }
    })
    print(f"Scam tx result: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Get alternatives
    print("\nGetting safe alternatives...")
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "get_safe_alternatives",
        "arguments": {
            "original_action": "swap tokens on unknown DEX",
            "risk_level": "HIGH"
        }
    })
    print(f"Alternatives: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_scam_detection()
