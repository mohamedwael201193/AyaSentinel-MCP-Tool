import os
import json
import logging
from hedera import (Client, AccountId, PrivateKey, TopicCreateTransaction, TopicMessageSubmitTransaction, Hbar)
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()

class HederaClient:
    def __init__(self):
        self.account_id = os.getenv('HEDERA_ACCOUNT_ID')
        self.private_key = os.getenv('HEDERA_PRIVATE_KEY')
        self.network = os.getenv('HEDERA_NETWORK', 'testnet')
        self.topic_id = None
        self.client = self._init_client()
        self._load_or_create_topic()

    def _init_client(self):
        if self.network == 'testnet':
            client = Client.forTestnet()
        else:
            client = Client.forMainnet()
        client.setOperator(AccountId.fromString(self.account_id), PrivateKey.fromString(self.private_key))
        return client

    def _load_or_create_topic(self):
        cache_file = '.hedera_cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                self.topic_id = data.get('topic_id')
        if not self.topic_id:
            try:
                tx = TopicCreateTransaction().setAdminKey(PrivateKey.fromString(self.private_key)).setSubmitKey(PrivateKey.fromString(self.private_key))
                receipt = tx.execute(self.client).getReceipt(self.client)
                self.topic_id = str(receipt.topicId)
                with open(cache_file, 'w') as f:
                    json.dump({'topic_id': self.topic_id}, f)
            except Exception as e:
                logging.error(f"Failed to create HCS topic: {e}")
                raise

    def log_risk_analysis(self, message: Dict[str, Any]):
        try:
            msg = json.dumps(message)
            submit_tx = TopicMessageSubmitTransaction().setTopicId(self.topic_id).setMessage(msg)
            submit_tx.execute(self.client)
            return {'status': 'logged', 'topic_id': self.topic_id}
        except Exception as e:
            logging.error(f"Hedera log_risk_analysis error: {e}")
            return {'status': 'error', 'error': str(e)}

    def verify_transaction_onchain(self, tx_data: Dict[str, Any]):
        # Simulate verification for demo
        try:
            # In production, query Hedera Mirror Node or explorer
            return {'verified': True, 'tx_data': tx_data}
        except Exception as e:
            logging.error(f"verify_transaction_onchain error: {e}")
            return {'verified': False, 'error': str(e)}

    def create_safety_token(self, to_address: str, amount: float):
        # Simulate SAFE token creation
        try:
            # In production, use Hedera Token Service
            return {'token': 'SAFE', 'to': to_address, 'amount': amount, 'status': 'created'}
        except Exception as e:
            logging.error(f"create_safety_token error: {e}")
            return {'status': 'error', 'error': str(e)}
