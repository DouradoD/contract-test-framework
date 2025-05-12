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
    expected = read_json_file(f'{consumer_contracts_dir_path}/mock-data.json')

    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('and-values'),
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
def test_build_contract_with_the_same_structure(contract_dir_path, consumer_contracts_dir_path):

    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('using-like'),
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

    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('using-like-with-less-required-elements'),
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


# Creating a contract to test the provider with LIKE values using and less required elements
def test_build_contract(contract_dir_path):

    pact = Consumer('contract-with-same-structure').has_pact_with(
        Provider('Provider'),
        pact_dir=f'{contract_dir_path}/contract-service',
        log_dir='./logs'
    )
    pact.start_service()
    atexit.register(pact.stop_service)
    path = '/accounts/v2/contracts'
    headers={
        "authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCVVdYcTRLanhPMUwxdTFTaENJVVNrdEk5aXRreFJ0X1Zzb3luelVvVGFFIn0.eyJleHAiOjE3NDcwODk5OTEsImlhdCI6MTc0NzA4NjM5MSwianRpIjoiYzhiMWEyMmMtMmY5Ni00ZTQ4LTlhYmItOTgzM2QzZjE5NzE3IiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2UvYXV0aC9yZWFsbXMvYmVlcy1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwN2Y1YjZjMy1jNGJjLTQyNGYtYjk2Ni1iOGEzYjUzNzNjNTciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhY2E5MTY2MS1hN2JlLTRmMDAtODhiNC1kNDBkMTU4MWNiM2MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1iZWVzLXJlYWxtIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjoiMTI3LjAuMC42Iiwicm9sZXMiOlsiTWVtYmVyc2hpcCIsIkFkbWluIiwiQWNjb3VudFJlbGF5LldyaXRlIiwiQ2F0ZWdvcnlSZWxheS5Xcml0ZSIsIkNoYXJnZVJlbGF5LldyaXRlIiwiQ29tYm9SZWxheS5Xcml0ZSIsIkNyZWRpdFJlbGF5LldyaXRlIiwiRGVhbFJlbGF5LldyaXRlIiwiRW1wdGllc1JlbGF5LldyaXRlIiwiRmlsZU1hbmFnZW1lbnRSZWxheS5Xcml0ZSIsIkludmVudG9yeVJlbGF5LldyaXRlIiwiSW52b2ljZVJlbGF5LldyaXRlIiwiSXRlbVJlbGF5LldyaXRlIiwiTG95YWx0eUJ1c2luZXNzUmVsYXkuV3JpdGUiLCJPcmRlclJlbGF5LldyaXRlIiwiUHJpY2VSZWxheS5Xcml0ZSIsIlByb2R1Y3RBc3NvcnRtZW50UmVsYXkuV3JpdGUiLCJQcm9tb3Rpb25SZWxheS5Xcml0ZSIsIkVuZm9yY2VtZW50UmVsYXkuV3JpdGUiLCJGb3JjZVZpc2l0cy5Xcml0ZSIsIkZvcmNlVWNjLldyaXRlIiwiQWNjb3VudEZpbmFuY2lhbC5Xcml0ZSIsIkFjY291bnRCYXNpYy5Xcml0ZSIsIkNhcmVBc3NldC5Xcml0ZSIsIlBhcnRuZXJJbnZvaWNlRmlsZS5Xcml0ZSIsIlJlYWQiLCJXcml0ZSIsImJlZXMtZGVsaXZlci1sb2F0LndyaXRlIiwiRGF0YUluZ2VzdGlvblBvcnRhbC5lbmZvcmNlbWVudHMuV3JpdGUiLCJDb21wYW55U2VydmljZXMuQURNSU4iLCJST0xFX0FETUlOIiwiUk9MRV9DVVNUT01FUiIsIkJFRVMuUkVDT01NRU5ERVIuUk9MRV9DVVNUT01FUiIsIkJFRVMuUkVDT01NRU5ERVIuV1JJVEUiLCJCRUVTLlBST0RVQ1QuUkVBRCIsIkJFRVMuUFJPRFVDVC5XUklURSIsIkdsb2JhbC5SZWFkIiwiQmVlc1N5bmMuQWxsRW50aXRpZXMuV3JpdGUiLCJSZXdhcmRzLmNoYWxsZW5nZXMtYWNjb3VudC5Xcml0ZSIsIlJld2FyZHMuY2hhbGxlbmdlcy1hY2NvdW50LkRlbGV0ZSIsIlJld2FyZHMuY2hhbGxlbmdlcy5Xcml0ZSIsIlJld2FyZHMuT3BlcmF0aW9uLldyaXRlIiwiUmV3YXJkcy5PcGVyYXRpb24uQWNjZXB0TTJNIl0sInZlbmRvcklkIjoiNDJlYWE4M2ItMWFlYS00Y2U5LWEzMzgtNjM3MjU4NTlkNDUwIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWFjYTkxNjYxLWE3YmUtNGYwMC04OGI0LWQ0MGQxNTgxY2IzYyIsImNsaWVudEFkZHJlc3MiOiIxMjcuMC4wLjYiLCJjbGllbnRfaWQiOiJhY2E5MTY2MS1hN2JlLTRmMDAtODhiNC1kNDBkMTU4MWNiM2MifQ.fz4_FZDShN_mGGDPMhQEhwIB3sIWyWYz3tOchIs6Zba56ewsXrkWiCIMxyGLWgVpXs51sAamASk8Wyh6dwDv2Cn1bk9WBAZ8USPDkfVE--nkQEZvybA7dzt5F3L7Z1BCl4sJLyzC-2VrQapEuNEcEvgt_T7bUdHQe05srwENMHQto-ABuJSziCcje1co6VG84DQ6bncQYnuRYmI9_l4ixnJ_Zp_rsOMB-QjmMLjFVlrAud4U41qKHltV7KRc1R1quWJkqXMTSrzDfCIDcTG03_llDCZ23xvlx-uAChqqG0tYL83caShgQ8NWk0J9v7Gc8SKbytGEwzXNxL5R1oB0zA",
        "country":"BR",
        "Content-Type":"application/json"    
        }
    query={
            'vendorId': '42eaa83b-1aea-4ce9-a338-63725859d450',
            'customerAccountId': '67228141490'
            }
    
    (
        pact
        .given(f'A user with id 1 exists')
        .upon_receiving(f'A request for user with id 1')
        .with_request(
            method='GET', 
            path=path,
            headers=headers
            )
        .will_respond_with(status=400)
    )

    with pact:
        
        response = requests.get(f"{pact.uri}{path}", headers=headers)

        assert response.status_code == 400
    
    pact.stop_service()