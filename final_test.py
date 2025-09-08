import requests
import json
import time

# URL of your deployed Render application
BASE_URL = "https://aya-sentinel-mcp.onrender.com"

def warm_up_server():
    """Sends a request to wake up the server if it's sleeping."""
    print(" Warming up the server... (This may take up to 30 seconds for a cold start)")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Server is awake and responsive.")
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
    except requests.exceptions.ReadTimeout:
        print(" Server is starting up (cold start), this is normal. Please wait.")
    except Exception as e:
        print(f"❌ Error warming up server: {e}")

def run_all_tests():
    """Runs a full suite of tests against the live API."""
    print("\n🚀 Running AyaSentinel Final Production Tests...")

    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    print("✅ Health check passed")

    # Test 2: Tools Listing
    print("\n2. Testing Tools Endpoint...")
    response = requests.get(f"{BASE_URL}/tools")
    assert response.status_code == 200
    assert len(response.json()['tools']) == 4
    print("✅ Tools listing passed")

    # Test 3: Scam Detection Performance
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
    result = response.json().get('result', {})
    assert result.get('risk_level') == 'CRITICAL'
    print(f"✅ Scam detected correctly (Response time: {response_time:.2f}ms)")

    # Test 4: Safe Transaction
    print("\n4. Testing Safe Transaction...")
    response = requests.post(f"{BASE_URL}/invoke", json={
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "hedera",
            "to_address": "0.0.12345", # Example safe Hedera address
            "value": 10
        }
    })
    assert response.status_code == 200
    result = response.json().get('result', {})
    assert result.get('risk_level') in ['LOW', 'MEDIUM']
    print("✅ Safe transaction identified")

    print("\n🎉 ALL PRODUCTION TESTS PASSED! Ready for submission!")
    print(f"📍 Your API is live and verified at: {BASE_URL}")

if __name__ == "__main__":
    warm_up_server()
    run_all_tests()
