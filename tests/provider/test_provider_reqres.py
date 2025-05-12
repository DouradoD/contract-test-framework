# provider/tests/test_verify.py
import os
from pact import Verifier
import pytest
import sys
import io

import requests
import logging
import http.client
import json
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)
os.environ['PACT_DEBUG'] = 'true'  # Gets more verbose output

os.environ["PYTHONIOENCODING"] = "utf-8"

PROVIDER_BASE_URL = "https://reqres.in/api"

def test_contract_provider(contract_dir_path):
    # Path to the contract file
    CONTRACT_PATH = os.path.join(contract_dir_path, 'users/contract-with-same-structure-and-values.json')
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