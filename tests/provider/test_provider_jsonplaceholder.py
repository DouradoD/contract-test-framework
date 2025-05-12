# provider/tests/test_verify.py
import json
import os
from pact import Verifier
import pytest
import sys
import io

import requests
os.environ["PYTHONIOENCODING"] = "utf-8"

PROVIDER_BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.parametrize("contract_name", 
                    ['contract-with-same-structure-and-values.json',
                     'contract-with-same-structure-using-like-with-less-required-elements.json',
                     'contract-with-same-structure-using-like.json'])
def test_provider_compliance(contract_name, contract_dir_path):
    # Path to the contract file
    CONTRACT_DIR = os.path.join(contract_dir_path, 'jsonplaceholder')
    CONTRACT_PATH = os.path.join(CONTRACT_DIR, contract_name)
    verifier = Verifier(
        provider='Provider',
        provider_base_url=PROVIDER_BASE_URL,
        # Enable UTF-8 output and disable colors (optional)
        pact_verifier_cli_path='pact-provider-verifier',
        enable_pending=False,
        publish_version='1.0.0',
        verbose=True  # Disable verbose to reduce special chars
    )
    
    # Run verification
    result, output = verifier.verify_pacts(
        CONTRACT_PATH,
        headers={'Accept': 'application/json; charset=utf-8'}
    )
    print(output)  # Debug output
    assert result == 0

def test_contract_provider(contract_dir_path):
    # Path to the contract file
    PROVIDER_BASE_URL = "https://services-sit.bees-platform.dev"

    CONTRACT_PATH = os.path.join(contract_dir_path, 'contract-service/contract-with-same-structure-provider.json')
    verifier = Verifier(
        provider='Provider',
        provider_base_url=PROVIDER_BASE_URL,
        # Enable UTF-8 output and disable colors (optional)
        pact_verifier_cli_path='pact-provider-verifier',
        enable_pending=False,
        publish_version='1.0.0',
        verbose=True  # Disable verbose to reduce special chars
    )
    
    # Run verification
    result, output = verifier.verify_pacts(CONTRACT_PATH)

    print(output)  # Debug output
    assert result == 0

def test_get():
    PROVIDER_BASE_URL = "https://services-sit.bees-platform.dev"

    # Run this before the pact verification
    response = requests.get(
    f"{PROVIDER_BASE_URL}/accounts/v2/contracts",
    headers={
        "authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCVVdYcTRLanhPMUwxdTFTaENJVVNrdEk5aXRreFJ0X1Zzb3luelVvVGFFIn0.eyJleHAiOjE3NDcwODk5OTEsImlhdCI6MTc0NzA4NjM5MSwianRpIjoiYzhiMWEyMmMtMmY5Ni00ZTQ4LTlhYmItOTgzM2QzZjE5NzE3IiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2UvYXV0aC9yZWFsbXMvYmVlcy1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIwN2Y1YjZjMy1jNGJjLTQyNGYtYjk2Ni1iOGEzYjUzNzNjNTciLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhY2E5MTY2MS1hN2JlLTRmMDAtODhiNC1kNDBkMTU4MWNiM2MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1iZWVzLXJlYWxtIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjoiMTI3LjAuMC42Iiwicm9sZXMiOlsiTWVtYmVyc2hpcCIsIkFkbWluIiwiQWNjb3VudFJlbGF5LldyaXRlIiwiQ2F0ZWdvcnlSZWxheS5Xcml0ZSIsIkNoYXJnZVJlbGF5LldyaXRlIiwiQ29tYm9SZWxheS5Xcml0ZSIsIkNyZWRpdFJlbGF5LldyaXRlIiwiRGVhbFJlbGF5LldyaXRlIiwiRW1wdGllc1JlbGF5LldyaXRlIiwiRmlsZU1hbmFnZW1lbnRSZWxheS5Xcml0ZSIsIkludmVudG9yeVJlbGF5LldyaXRlIiwiSW52b2ljZVJlbGF5LldyaXRlIiwiSXRlbVJlbGF5LldyaXRlIiwiTG95YWx0eUJ1c2luZXNzUmVsYXkuV3JpdGUiLCJPcmRlclJlbGF5LldyaXRlIiwiUHJpY2VSZWxheS5Xcml0ZSIsIlByb2R1Y3RBc3NvcnRtZW50UmVsYXkuV3JpdGUiLCJQcm9tb3Rpb25SZWxheS5Xcml0ZSIsIkVuZm9yY2VtZW50UmVsYXkuV3JpdGUiLCJGb3JjZVZpc2l0cy5Xcml0ZSIsIkZvcmNlVWNjLldyaXRlIiwiQWNjb3VudEZpbmFuY2lhbC5Xcml0ZSIsIkFjY291bnRCYXNpYy5Xcml0ZSIsIkNhcmVBc3NldC5Xcml0ZSIsIlBhcnRuZXJJbnZvaWNlRmlsZS5Xcml0ZSIsIlJlYWQiLCJXcml0ZSIsImJlZXMtZGVsaXZlci1sb2F0LndyaXRlIiwiRGF0YUluZ2VzdGlvblBvcnRhbC5lbmZvcmNlbWVudHMuV3JpdGUiLCJDb21wYW55U2VydmljZXMuQURNSU4iLCJST0xFX0FETUlOIiwiUk9MRV9DVVNUT01FUiIsIkJFRVMuUkVDT01NRU5ERVIuUk9MRV9DVVNUT01FUiIsIkJFRVMuUkVDT01NRU5ERVIuV1JJVEUiLCJCRUVTLlBST0RVQ1QuUkVBRCIsIkJFRVMuUFJPRFVDVC5XUklURSIsIkdsb2JhbC5SZWFkIiwiQmVlc1N5bmMuQWxsRW50aXRpZXMuV3JpdGUiLCJSZXdhcmRzLmNoYWxsZW5nZXMtYWNjb3VudC5Xcml0ZSIsIlJld2FyZHMuY2hhbGxlbmdlcy1hY2NvdW50LkRlbGV0ZSIsIlJld2FyZHMuY2hhbGxlbmdlcy5Xcml0ZSIsIlJld2FyZHMuT3BlcmF0aW9uLldyaXRlIiwiUmV3YXJkcy5PcGVyYXRpb24uQWNjZXB0TTJNIl0sInZlbmRvcklkIjoiNDJlYWE4M2ItMWFlYS00Y2U5LWEzMzgtNjM3MjU4NTlkNDUwIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWFjYTkxNjYxLWE3YmUtNGYwMC04OGI0LWQ0MGQxNTgxY2IzYyIsImNsaWVudEFkZHJlc3MiOiIxMjcuMC4wLjYiLCJjbGllbnRfaWQiOiJhY2E5MTY2MS1hN2JlLTRmMDAtODhiNC1kNDBkMTU4MWNiM2MifQ.fz4_FZDShN_mGGDPMhQEhwIB3sIWyWYz3tOchIs6Zba56ewsXrkWiCIMxyGLWgVpXs51sAamASk8Wyh6dwDv2Cn1bk9WBAZ8USPDkfVE--nkQEZvybA7dzt5F3L7Z1BCl4sJLyzC-2VrQapEuNEcEvgt_T7bUdHQe05srwENMHQto-ABuJSziCcje1co6VG84DQ6bncQYnuRYmI9_l4ixnJ_Zp_rsOMB-QjmMLjFVlrAud4U41qKHltV7KRc1R1quWJkqXMTSrzDfCIDcTG03_llDCZ23xvlx-uAChqqG0tYL83caShgQ8NWk0J9v7Gc8SKbytGEwzXNxL5R1oB0zA",
        "country":"BR",
        "Content-Type":"application/json"    
        }
    )
    print("\nACTUAL API RESPONSE:")
    print(f"Status: {response.status_code}")
    print("Headers received:", response.headers)
    print("Body:", json.dumps(response.json(), indent=2))
