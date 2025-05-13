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
