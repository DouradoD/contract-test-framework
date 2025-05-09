# provider/tests/test_verify.py
import os
from pact import Verifier
import sys
import io
from consumer.tests.test_create_contracts import test_get_country_contract
os.environ["PYTHONIOENCODING"] = "utf-8"
# Force UTF-8 encoding (Windows fix)
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Get directory of current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up to project root (adjust number of dirname calls as needed)
project_root = os.path.dirname(os.path.dirname(current_dir))

# Path to the contract file
CONTRACT_DIR = os.path.join(project_root, 'broker', 'contracts')
CONTRACT_PATH = os.path.join(CONTRACT_DIR, 'consumer-provider.json')
PROVIDER_BASE_URL = "https://jsonplaceholder.typicode.com"


def test_provider_compliance():
    test_get_country_contract()
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