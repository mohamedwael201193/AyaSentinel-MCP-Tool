# server/services/hedera_service.py

import os
import json
import logging
from hedera import (
    Client,
    PrivateKey,
    TopicMessageSubmitTransaction,
    TopicId
)

# Setup a logger for this service
logger = logging.getLogger(__name__)

def get_hedera_client() -> Client:
    """
    Configures and returns a Hedera client for the specified network (testnet).
    Raises Exception if environment variables are not set.
    """
    account_id = os.getenv("HEDERA_ACCOUNT_ID")
    private_key_str = os.getenv("HEDERA_PRIVATE_KEY")

    if not account_id or not private_key_str:
        logger.error("Hedera credentials (ACCOUNT_ID, PRIVATE_KEY) are not set.")
        raise ValueError("HEDERA_ACCOUNT_ID and HEDERA_PRIVATE_KEY must be set.")

    # Remove "0x" prefix if it exists from the private key
    if private_key_str.startswith("0x"):
        private_key_str = private_key_str[2:]

    private_key = PrivateKey.fromString(private_key_str)

    client = Client.forTestnet()
    client.setOperator(account_id, private_key)
    return client

def log_analysis_to_hcs(analysis_payload: dict) -> str | None:
    """
    Logs the analysis result as a message to a topic on the Hedera Consensus Service.

    Args:
        analysis_payload: A dictionary containing the analysis data to be logged.

    Returns:
        The transaction ID as a string if successful, otherwise None.
    """
    try:
        client = get_hedera_client()
        topic_id_str = os.getenv("HEDERA_TOPIC_ID")

        if not topic_id_str:
            logger.error("HEDERA_TOPIC_ID is not set in environment variables.")
            raise ValueError("HEDERA_TOPIC_ID must be set.")
        
        topic_id = TopicId.fromString(topic_id_str)

        # Convert the analysis result dictionary to a JSON string for submission
        message_content = json.dumps(analysis_payload, indent=2)

        logger.info(f"Submitting to HCS Topic {topic_id_str}...")

        # Create and execute the transaction to submit the message
        transaction = TopicMessageSubmitTransaction().setTopicId(topic_id).setMessage(message_content)
        
        submit_response = transaction.execute(client)
        
        # Get the receipt to confirm the transaction was successful
        receipt = submit_response.getReceipt(client)
        
        transaction_id = str(submit_response.transactionId)
        logger.info(f"Successfully submitted to HCS. Transaction ID: {transaction_id}")
        
        return transaction_id

    except Exception as e:
        logger.error(f"Failed to submit message to Hedera HCS: {e}", exc_info=True)
        return None