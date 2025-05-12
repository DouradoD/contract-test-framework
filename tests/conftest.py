import pytest
import os
from pathlib import Path

@pytest.fixture(scope='session')
def contract_dir_path():
    # Create the contract directory path thorgh the current file's parent directory
    CONTRACT_DIR = Path(__file__).parent.parent / 'broker' / 'contracts'
    return CONTRACT_DIR