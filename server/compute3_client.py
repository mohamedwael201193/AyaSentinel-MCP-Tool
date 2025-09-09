# server/comput3_client.py

import os
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class Comput3Client:
    """
    Client for making REAL API calls to the Comput3.ai service for transaction analysis.
    """
    def __init__(self, api_key: Optional[str]):
        if not api_key:
            logger.error("COMPUT3_API_KEY is required but was not provided.")
            raise ValueError("COMPUT3_API_KEY is required.")
        
        self.api_key = api_key
        self.base_url = os.getenv('COMPUT3_BASE_URL', 'https://api.comput3.ai/v1')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def analyze_transaction(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends transaction data to the Comput3.ai API for real-time risk analysis.
        """
        try:
            # Prepare the payload for the API call.
            payload = {
                "chain": arguments.get("chain"),
                "to": arguments.get("to_address"),
                "from": arguments.get("from_address"),
                "value": str(arguments.get("value")),
                "data": arguments.get("data", "")
            }
            
            logger.info(f"Sending analysis request to Comput3.ai for address: {payload['to']}")

            # Make the actual API call to the transaction analysis endpoint.
            response = requests.post(
                f"{self.base_url}/analysis/transaction",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()
            
            logger.info("Successfully received a valid response from Comput3.ai.")
            
            # Return the 'result' part of the JSON response.
            return response.json().get('result', {})

        except requests.exceptions.RequestException as e:
            logger.error(f"Comput3.ai API call failed: {e}")
            # Return a clear error message if the service cannot be reached.
            return {
                "error": True,
                "message": "Failed to connect to the AI analysis service. Please try again later.",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"An unexpected error occurred in Comput3Client: {e}", exc_info=True)
            return {
                "error": True,
                "message": "An unexpected internal error occurred.",
                "details": str(e)
            }