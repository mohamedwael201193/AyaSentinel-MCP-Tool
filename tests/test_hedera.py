import requests
import time

def get_topic_messages():
    # This function needs to be implemented.
    # It should query the hedera mirror node for messages on the topic
    # and return a list of messages.
    # For now, it returns an empty list.
    print("Warning: get_topic_messages() is not implemented. Test will fail.")
    return []

def test_topic_write():
    payload = {"foo": "bar"}
    try:
        r = requests.post("http://localhost:8080/api/scan/transaction", json=payload, timeout=10)
        r.raise_for_status()
        tx_hash = r.json()["txHash"]
        # Wait ≤10 s for mirror node
        for _ in range(10):
            time.sleep(1)
            if tx_hash in get_topic_messages():
                return
        raise AssertionError("Hash not found on-chain")
    except requests.exceptions.ConnectionError as e:
        print("Connection to the server failed. Please ensure the server is running.")
        raise e
