import os
import requests
import atexit
from pact import Consumer, Provider
from helpers.helper import read_json_file
 
# Get directory of current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up to project root (adjust number of dirname calls as needed)
project_root = os.path.dirname(os.path.dirname(current_dir))

# Path to the contract file
CONTRACT_DIR = os.path.join(project_root, 'broker', 'contracts')
CONTRACT_FILE = os.path.join(CONTRACT_DIR, 'consumer_provider.json')


pact = Consumer('Consumer').has_pact_with(
    Provider('Provider'),
    pact_dir=CONTRACT_DIR,
    log_dir='./logs'
)
pact.start_service()
atexit.register(pact.stop_service)

# Configuration
API_BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_country_contract():
    expected = read_json_file('consumer/consumer_contracts/mock-data.json')
    
    (
        pact
        .given(f'A user with id 1 exists')
        .upon_receiving(f'A request for user with id 1')
        .with_request(
            method='GET', 
            path=f'/posts/100', 
            headers={
                  "Host": "localhost:1234",
                  "User-Agent": "python-requests/2.32.3",
                  "Accept-Encoding": "gzip, deflate",
                  "Accept": "*/*",
                  "Connection": "keep-alive",
                  "Version": "HTTP/1.1"
                }
            )
        .will_respond_with(200, body=expected)
    )

    with pact:
        response = requests.get(f"{pact.uri}/posts/100")
        assert response.status_code == 200
        assert response.json() == expected