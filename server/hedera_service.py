# server/hedera_service.py
import os
import logging

logger = logging.getLogger(__name__)

# Use the mock client that doesn't require Java
from .hedera_mock import MockHederaClient

def init_hedera():
    """Initialize the Hedera client (mock for now, no Java required)"""
    return MockHederaClient()

hedera_client = init_hedera()
