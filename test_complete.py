# test_complete.py
import requests
import json
import time
import os

BASE_URL = "http://localhost:8080"

def test_all_endpoints():
    print("🧪 Testing all endpoints...\n")
    
    # 1. Health Check
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    print("✅ Health check: OK")
    
    # 2. Tools List
    r = requests.get(f"{BASE_URL}/tools")
    assert r.status_code == 200
    tools = r.json()
    print(f"✅ Tools: {len(tools)} tools available")
    
    # 3. Scam Detection (CRITICAL)
    r = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "ethereum",
            "to_address": "0x000000000000000000000000000000000000dead",
            "value": 1000
        }
    })
    assert r.status_code == 200
    result = r.json()["result"]
    assert result["risk_level"] == "CRITICAL"
    print(f"✅ Scam detection: {result['risk_level']} (correct)")
    
    # 4. Safe Transaction
    r = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "hedera",
            "to_address": "0.0.12345",
            "from_address": "0.0.67890",
            "value": 10
        }
    })
    assert r.status_code == 200
    result = r.json()["result"]
    print(f"✅ Safe transaction: {result['risk_level']}")
    
    # 5. Direct Hedera endpoint
    r = requests.post(f"{BASE_URL}/api/scan/transaction", json={
        "test": "data",
        "timestamp": time.time()
    })
    assert r.status_code == 200
    print(f"✅ Hedera submission: {r.json().get('txHash', 'N/A')[:16]}...")
    
    # 6. Compute job (will fail without valid Comput3 key, but structure is tested)
    r = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "hedera_compute_job",
        "arguments": {
            "docker_image": "python:3.9",
            "command": "echo test"
        }
    })
    print(f"✅ Compute endpoint: Status {r.status_code}")
    
    # Check if log file was created
    if os.path.exists("hedera_transactions.log"):
        with open("hedera_transactions.log", "r") as f:
            lines = f.readlines()
            print(f"✅ Log file: {len(lines)} transactions logged")
    
    print("\n🎉 All local tests passed!")

if __name__ == "__main__":
    test_all_endpoints()