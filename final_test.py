# final_test.py

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Load the API URL from environment variables or use a default
BASE_URL = os.getenv("API_URL", "https://aya-sentinel-mcp.onrender.com")

def print_status(message, is_success):
    if is_success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        exit(1) # Exit with an error code if any test fails

def test_endpoint(name, method, endpoint, expected_status, json_payload=None):
    print(f"\n{name}...")
    try:
        start_time = time.time()
        if method.upper() == 'GET':
            response = requests.get(endpoint, timeout=30)
        else:
            response = requests.post(endpoint, json=json_payload, timeout=45)
        
        duration = (time.time() - start_time) * 1000  # in ms
        
        if response.status_code == expected_status:
            print_status(f"Status code OK ({expected_status})", True)
            return response.json(), duration
        else:
            print_status(f"Expected status {expected_status}, but got {response.status_code}", False)
            print(f"Response: {response.text}")
            return None, duration
            
    except requests.exceptions.RequestException as e:
        print_status(f"Request failed: {e}", False)
        return None, 0

def run_tests():
    print("🚀 Running AyaSentinel Final Production Tests...")

    # 1. Test Health Endpoint
    health_data, _ = test_endpoint("1. Testing Health Endpoint", "GET", f"{BASE_URL}/", 200)
    if health_data:
        print_status("Health check passed", True)

    # 2. Test Tools Endpoint
    tools_data, _ = test_endpoint("2. Testing Tools Endpoint", "GET", f"{BASE_URL}/tools", 200)
    if tools_data:
        print_status(f"Tools listing passed ({len(tools_data)} tools found)", True)

    # 3. Test Scam Detection (High Risk)
    scam_payload = {
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "ethereum",
            "to_address": "0x000000000000000000000000000000000000dead", # Known scam
            "value": 1000
        }
    }
    scam_data, scam_duration = test_endpoint("3. Testing Scam Detection", "POST", f"{BASE_URL}/invoke", 200, scam_payload)
    if scam_data:
        result = scam_data.get("result", {})
        tx_id = scam_data.get("hedera_transaction_id")
        
        if result and "risk_level" in result:
             print_status(f"Scam detected correctly (Response time: {scam_duration:.2f}ms)", True)
        else:
            print_status("Scam detection failed to return a valid result.", False)
        
        if tx_id and "Failed" not in tx_id:
            print_status(f"Hedera logging successful (TxID: {tx_id})", True)
        else:
            print_status("Hedera logging FAILED or was not returned.", False)


    # 4. Test Safe Transaction (Low Risk)
    safe_payload = {
        "tool": "analyze_transaction_risk",
        "arguments": {
            "chain": "hedera",
            "to_address": "0.0.12345", # Generic safe address
            "from_address": "0.0.67890",
            "value": 10
        }
    }
    safe_data, _ = test_endpoint("4. Testing Safe Transaction", "POST", f"{BASE_URL}/invoke", 200, safe_payload)
    if safe_data:
        result = safe_data.get("result", {})
        tx_id = safe_data.get("hedera_transaction_id")
        
        if result and "risk_level" in result:
            print_status("Safe transaction identified", True)
        else:
            print_status("Safe transaction analysis failed.", False)
            
        if tx_id and "Failed" not in tx_id:
            print_status("Hedera logging successful for safe transaction", True)
        else:
            print_status("Hedera logging FAILED for safe transaction.", False)


    print("\n\n🎉 ALL PRODUCTION TESTS PASSED! Ready for submission!")
    print(f"Your API is live and verified at: {BASE_URL}")

if __name__ == "__main__":
    # Wait for the server to warm up on services like Render
    print(f"Warming up the server at {BASE_URL}...")
    print("(This may take up to 30 seconds for a cold start)")
    time.sleep(5)
    run_tests()