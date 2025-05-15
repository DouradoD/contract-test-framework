import requests
import atexit
from pact import Consumer, Like, Provider
from helpers.helper import read_json_file


# Creating a contract to test the provider with the same values using the mock-data.json file
def test_build_contract_with_the_same_structure_and_values(contract_dir_path, consumer_contracts_dir_path):
    expected = read_json_file(f'{consumer_contracts_dir_path}/jsonplaceholder/mock-data.json')

    pact = Consumer('consumer-get-success-1').has_pact_with(
        Provider('provider-jsonplaceholder'),
        pact_dir=f'{contract_dir_path}/jsonplaceholder',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
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
        .will_respond_with(
            status=200, 
            body=expected)
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/posts/100")

        assert response.status_code == 200
        assert response.json() == expected
    
    pact.stop_service()

# Creating a contract to test the provider with LIKE values using Only the same structure
def test_build_contract_with_the_same_structure(contract_dir_path):

    pact = Consumer('consumer-get-success-2').has_pact_with(
        Provider('provider-jsonplaceholder'),
        pact_dir=f'{contract_dir_path}/jsonplaceholder',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
        .upon_receiving(f'A request for user with id 1')
        .with_request(
            method='GET', 
            path=f'/posts/100', 
            headers={
                  "Host": "localhost:1234", # Default values, not required
                  "User-Agent": "python-requests/2.32.3", # Default values, not required
                  "Accept-Encoding": "gzip, deflate", # Default values, not required
                  "Accept": "*/*", # Default values, not required
                  "Connection": "keep-alive", # Default values, not required
                  "Version": "HTTP/1.1", # Default values, not required
                  "Content-Type": "application/json"
                }
            )
        .will_respond_with(
            status=200, 
            body=Like({
                "userId": 0,
                "id": 0,
                "title": "String",
                "body": "String"
            })
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/posts/100", headers={"Content-Type": "application/json"})

        assert response.status_code == 200
    
    pact.stop_service()


# Creating a contract to test the provider with LIKE values using and less required elements
def test_build_contract_with_less_required_elements(contract_dir_path, consumer_contracts_dir_path):

    pact = Consumer('consumer-get-success-3').has_pact_with(
        Provider('provider-jsonplaceholder'),
        pact_dir=f'{contract_dir_path}/jsonplaceholder',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
        .given(f'A user with id 1 exists')
        .upon_receiving(f'A request for user with id 1')
        .with_request(
            method='GET', 
            path='/posts/100'
            )
        .will_respond_with(
            status=200, 
            body=Like({
                "userId": 0,
                "id": 0,
                "body": "String"
            })
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/posts/100")

        assert response.status_code == 200
    
    pact.stop_service()
