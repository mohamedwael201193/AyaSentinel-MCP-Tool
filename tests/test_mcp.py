import pytest
import json
from server.mcp_server import MCPServer
from server.scam_detector import ScamDetector

@pytest.fixture
def client():
    server = MCPServer()
    server.app.config['TESTING'] = True
    return server.app.test_client()

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'healthy'

def test_tools_endpoint(client):
    response = client.get('/tools')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tools' in data
    assert len(data['tools']) == 4

def test_analyze_transaction_risk(client):
    payload = {
        'tool': 'analyze_transaction_risk',
        'arguments': {
            'chain': 'ethereum',
            'to_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
            'from_address': '0x123',
            'value': 100
        }
    }
    response = client.post('/invoke', json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'result' in data
    assert 'risk_score' in data['result']

def test_known_scam_detection(client):
    payload = {
        'tool': 'analyze_transaction_risk',
        'arguments': {
            'chain': 'ethereum',
            'to_address': '0x000000000000000000000000000000000000dead',
            'value': 100
        }
    }
    response = client.post('/invoke', json=payload)
    data = json.loads(response.data)
    assert data['result']['risk_level'] == 'CRITICAL'

def test_hedera_integration():
    from server.hedera_client import HederaClient
    hedera = HederaClient()
    result = hedera.verify_transaction_onchain({'test': 'data'})
    assert 'verified' in result

def test_compute3_integration():
    from server.compute3_client import Compute3Client
    compute3 = Compute3Client()
    result = compute3.run_scam_detection_model({
        'to_address': '0x123',
        'value': 100,
        'chain': 'ethereum'
    })
    assert 'risk_score' in result
