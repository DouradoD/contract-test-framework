import os
import requests
import atexit
from pact import Consumer, Like, Provider
from helpers.helper import read_json_file

def create_jsonplaceholder_directory(contract_dir_path):
    pact_dir_path = os.path.join(contract_dir_path, 'jsonplaceholder')
    pact_dir_path.mkdir(parents=True, exist_ok=True)

# Creating a contract to test the provider with the same values using the mock-data.json file
def test_build_contract_with_the_same_structure_and_values(contract_dir_path, consumer_contracts_dir_path):
    expected = {"data":{"id":2,"email":"janet.weaver@reqres.in","first_name":"Janet","last_name":"Weaver","avatar":"https://reqres.in/img/faces/2-image.jpg"},"support":{"url":"https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral","text":"Tired of writing endless social media content? Let Content Caddy generate it for you."}}


    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('and-values'),
        pact_dir=f'{contract_dir_path}/users',
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
            path='/users/2'
            )
        .will_respond_with(
            status=200, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/users/2")

        assert response.status_code == 200
        assert response.json() == expected
    
    pact.stop_service()


