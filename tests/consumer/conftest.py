import pytest
import os
from pathlib import Path
from pact import Consumer, Provider

"""
Fixture scopes
Fixtures are created when first requested by a test, and are destroyed based on their scope:

function: the default scope, the fixture is destroyed at the end of the test.

class: the fixture is destroyed during teardown of the last test in the class.

module: the fixture is destroyed during teardown of the last test in the module.

package: the fixture is destroyed during teardown of the last test in the package.

session: the fixture is destroyed at the end of the test session.
"""

@pytest.fixture(scope='session')
def consumer_contracts_dir_path():
    # Get directory of current file
    CONTRACT_DIR = Path(__file__).parent / 'consumer_contracts'
    # Go up to project root (adjust number of dirname calls as needed)
    return CONTRACT_DIR