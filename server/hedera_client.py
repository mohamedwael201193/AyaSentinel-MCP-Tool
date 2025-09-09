# server/hedera_client.py
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from hedera import (
    Client,
    PrivateKey,
    TopicMessageSubmitTransaction,
    TopicId,
    AccountId
)

load_dotenv()
logger = logging.getLogger("AyaSentinel.HederaClient")

class HederaClient:
    def __init__(self):
        self.account_id_str = os.getenv('HEDERA_ACCOUNT_ID')
        self.private_key_str = os.getenv('HEDERA_PRIVATE_KEY')
        self.topic_id_str = os.getenv('HEDERA_TOPIC_ID')
        self.network = os.getenv('HEDERA_NETWORK', 'testnet')
        self.environment = os.getenv('ENVIRONMENT', 'development')

        if not all([self.account_id_str, self.private_key_str, self.topic_id_str]):
            raise Exception("FATAL: HEDERA_ACCOUNT_ID, HEDERA_PRIVATE_KEY, and HEDERA_TOPIC_ID must be set.")

        if self.network == 'mainnet':
            self.client = Client.forMainnet()
        else:
            self.client = Client.forTestnet()
        
        # --- THE CRITICAL FIX ---
        # Use the ECDSA format for the raw private key, which we proved works.
        self.private_key = PrivateKey.fromStringECDSA(self.private_key_str)
        # ------------------------
        
        self.account_id = AccountId.fromString(self.account_id_str)
        self.topic_id = TopicId.fromString(self.topic_id_str)
        self.client.setOperator(self.account_id, self.private_key)
        
        logger.info(f"HederaClient initialized for account {self.account_id} on {self.network} in '{self.environment}' mode.")

    def log_risk_analysis(self, analysis_data: dict) -> dict:
        if self.environment != 'production':
            logger.info(f"Skipping REAL HCS submission because ENVIRONMENT is '{self.environment}'.")
            return {"success": True, "message": "Simulated HCS submission (not in production mode)."}
            
        try:
            message_to_submit = json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "analysis": analysis_data,
                "version": "1.5.0-final", 
            })

            logger.info(f"Submitting REAL message to HCS Topic {self.topic_id_str}...")
            transaction = TopicMessageSubmitTransaction().setTopicId(self.topic_id).setMessage(message_to_submit)
            receipt = transaction.freezeWith(self.client).sign(self.private_key).execute(self.client).getReceipt()
            sequence_number = receipt.topicSequenceNumber
            
            logger.info(f"SUCCESS! Message submitted to HCS. Sequence number: {sequence_number}")
            return {"success": True, "sequence_number": sequence_number}

        except Exception as e:
            logger.error(f"FATAL ERROR: Failed to submit message to HCS: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def verify_transaction_onchain(self, tx_data: dict) -> dict:
        # Placeholder for demo
        return {"verified": True, "message": "Verification logic placeholder."}

