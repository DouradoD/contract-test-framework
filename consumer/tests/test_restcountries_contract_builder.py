import requests
import atexit
from pact import Consumer, EachLike, Like, Provider, Term


# Creating a contract to test the provider with the same values using the mock-data.json file
def test_build_contract_with_the_same_structure_and_values(contract_dir_path):
    expected = EachLike({
    "name": {
        "common": Like("Brazil"),
        "official": Like("Federative Republic of Brazil"),
        "nativeName": {
            "por": {
                "official": Term(r"[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+", "República Federativa do Brasil"),
                "common": Term(r"[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+", "Brasil")
            }
        }
    }
})
    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('and-values'),
        pact_dir=f'{contract_dir_path}/countries',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)

    headers={'content-type':'application/json'}
    query = {'test': '1'}
    
    (
        pact
        .given(f'A country with name Brazil exists')
        .upon_receiving(f'A request for countries with name Brazil')
        .with_request(
            method='GET', 
            path='/name/brazil',
            headers=headers,
            query=query
            )
        .will_respond_with(
            status=200, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/name/brazil", headers=headers, params=query)

        assert response.status_code == 200
    
    pact.stop_service()

# Creating a contract to test the provider with the same values using the mock-data.json file
def test_build_contract_with_invalid_values(contract_dir_path):
    expected = {"message":"Not Found","status":404}

    pact = Consumer('bad-request-consumer').has_pact_with(
        Provider('provider'),
        pact_dir=f'{contract_dir_path}/countries',
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
            path='/name/3'
            )
        .will_respond_with(
            status=404, 
            body=Like(expected)
            )
    )

    with pact:
        
        response = requests.get(f"{pact.uri}/name/3")

        assert response.status_code == 404
        assert response.json() == expected
    
    pact.stop_service()

def get():
    response = requests.get(url='https://restcountries.com/v3.1')
    print(response.json())
