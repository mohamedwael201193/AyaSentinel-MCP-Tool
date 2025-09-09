# verify_setup.py
import os
from dotenv import load_dotenv
load_dotenv()

# Test import
try:
    from hedera import Client, TopicId
    print("✅ Hedera SDK imported successfully (no Java needed!)")
    
    # Test client creation
    client = Client.for_testnet()
    client.set_operator(
        os.getenv("HEDERA_ACCOUNT_ID"),
        os.getenv("HEDERA_PRIVATE_KEY")
    )
    print("✅ Client initialized")
    
    # Test topic ID parsing
    topic = TopicId.from_string(os.getenv("HEDERA_TOPIC_ID"))
    print(f"✅ Topic ID parsed: {topic}")
    
except Exception as e:
    print(f"❌ Error: {e}")
