# provider/tests/test_verify.py
import os
from pact import Verifier
import pytest
import logging
import http.client

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)
os.environ['PACT_DEBUG'] = 'true'  # Gets more verbose output

os.environ["PYTHONIOENCODING"] = "utf-8"

PROVIDER_BASE_URL = "https://restcountries.com/v3.1"


@pytest.mark.parametrize("contract_name", 
                    ['contract-with-same-structure-and-values.json',
                     'bad-request-consumer-provider.json'])
def test_contract_provider(contract_dir_path, contract_name):
    # Path to the contract file
    CONTRACT_DIR = os.path.join(contract_dir_path, 'countries')
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
    result, output = verifier.verify_pacts(CONTRACT_PATH)

    print(output)  # Debug output
    assert result == 0