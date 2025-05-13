import requests
import atexit
from pact import Consumer, Like, Provider

# Creating a contract to test the provider with the same values using the mock-data.json file
def test_pet_get_say_hello(contract_dir_path):
    expected = {"message": "Hello!"}

    pact = Consumer('consumer-say-hello').has_pact_with(
        Provider('provider'),
        pact_dir=f'{contract_dir_path}/petapi_contracts',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
        .given(f'A service check if available ')
        .upon_receiving(f'A request for get Say Hello')
        .with_request(
            method='GET', 
            path='/'
            )
        .will_respond_with(
            status=200, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/")

        assert response.status_code == 200
        assert response.json() == expected
    
    pact.stop_service()

def test_pet_get_by_id(contract_dir_path):
    pet_id = 1
    expected = {"category": "dog","id": pet_id,"name": "Bug"}

    pact = Consumer('consumer-get-pet').has_pact_with(
        Provider('provider'),
        pact_dir=f'{contract_dir_path}/petapi_contracts',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
        .given(f'A user checking the pet with id {pet_id}')
        .upon_receiving(f'A request for get pet with id {pet_id}')
        .with_request(
            method='GET', 
            path=f'/pets/{pet_id}'
            )
        .will_respond_with(
            status=200, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/pets/{pet_id}")

        assert response.status_code == 200
        assert response.json() == expected
    
    pact.stop_service()

def test_path_pet_by_id(contract_dir_path):
    pet_id = 1
    expected = {"category": "dog","id": pet_id,"name": "Bold"}

    pact = Consumer('consumer-pacth-pet').has_pact_with(
        Provider('provider'),
        pact_dir=f'{contract_dir_path}/petapi_contracts',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    
    (
        pact
        .given(f'A user updating the pet name with id {pet_id}')
        .upon_receiving(f'A request for patch the pet name by id {pet_id}')
        .with_request(
            method='PATCH', 
            path=f'/pets/{pet_id}'
            )
        .will_respond_with(
            status=200, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.patch(f"{pact.uri}/pets/{pet_id}")

        assert response.status_code == 200
        assert response.json() == expected
    
    pact.stop_service()