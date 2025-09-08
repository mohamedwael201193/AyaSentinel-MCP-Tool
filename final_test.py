import requests
import json
import time


BASE_URL = "https://aya-sentinel-mcp.onrender.com"
# For local testing use: BASE_URL = "http://192.168.1.18:8080"

def run_all_tests():
    print("🚀 Running AyaSentinel Final Tests...")
    
    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")
    
    # Test 2: Tools Listing
    print("\n2. Testing Tools Endpoint...")
    response = requests.get(f"{BASE_URL}/tools")
    assert response.status_code == 200
    assert len(response.json()['tools']) == 4
    print("✅ Tools listing passed")
    
    # Test 3: Scam Detection
    print("\n3. Testing Scam Detection...")
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "ethereum",
            "to_address": "0x000000000000000000000000000000000000dead",
            "value": 1000
        }
    })
    response_time = (time.time() - start_time) * 1000
    
    assert response.status_code == 200
    result = response.json()['result']
    assert result['risk_level'] == 'CRITICAL'
    print(f"✅ Scam detected correctly (Response time: {response_time:.2f}ms)")
    
    # Test 4: Safe Transaction
    print("\n4. Testing Safe Transaction...")
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "hedera",
            "to_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "value": 10
        }
    })
    assert response.status_code == 200
    result = response.json()['result']
    assert result['risk_level'] in ['LOW', 'MEDIUM']
    print("✅ Safe transaction identified")
    
    print("\n🎉 ALL TESTS PASSED! Ready for submission!")
    print(f"📍 Your API is live at: {BASE_URL}")

if __name__ == "__main__":
    run_all_tests()
