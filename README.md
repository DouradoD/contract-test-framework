# Contract Test Framework

This project is a contract testing framework designed to validate interactions between a consumer and a provider using the Pact framework.

Helper: https://docs.pact.io/implementation_guides/python

---

## Folder Structure

```
contract-test-framework/
├── broker/                          # Acts as local Pact Broker
│   └── contracts/                   
│       └── folders                  # Generated contract files -> This folders are generated during the contract builder(consumer) execution
│            └── consumer-provider.json   # Example contract
│
├── consumer/
│   ├── contracts/                   # Consumer contract definitions
│   │   ├── jsonplaceholder/         # Organized by endpoint
│   │       └── mock-data.json       # Example mock response
│   │
│   └── tests/
│       ├── contract_tests/          # Pact contract tests builder
│       │   └── test_country_api_builder_contract.py
│       └── conftest.py/             # Pytest setup
│
├── provider/
│   └── tests/
│       │   └── verify_contracts.py  # Provider code
│       └── conftest.py/             # Pytest setup
│
├── .vscode/
│   └── launch.json                  # Debug configs
│
├── config/ TBD/WIP
│   ├── pact-config.yml              # Pact CLI configuration
│   └── test-config.yml              # Environment configs
│
├── scripts/ TBD/WIP
│   ├── publish_contracts.sh         # CI scripts
│   └── verify_contracts.sh
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Pact test environment TBD
├── docker-compose.yml               # Service definitions TBD
├── pytest.init                      # Define the 
└── README.md                        # SET PYTHONPATH to pytest
```

# Notes and Considerations
```
While pact-python is a powerful tool for contract testing, there are several challenges and limitations to be aware of:

Log Clarity:

It can be difficult to analyze logs and pinpoint errors during test execution.
Logs often lack sufficient detail, especially when debugging issues with real APIs.
Using Real APIs:

When testing against a real API, the likelihood of encountering errors increases.
However, the logs remain insufficiently detailed, making it harder to identify the root cause of failures.
--provider-states-setup-url:

The purpose and usage of the --provider-states-setup-url attribute are not well-documented.
It is unclear what should be passed to this attribute, leading to confusion during setup.
Documentation:

The official documentation for pact-python could be improved with more comprehensive examples and clearer explanations.
Reference: Pact Python Documentation
Deprecation Warnings:

Many classes and methods in pact-python are marked for deprecation, which may require significant refactoring in the future.

```

## Requirements

- Python 3.8 or higher.

## Installation

1. Clone the repository.
2. Navigate to the project's root directory.
3. Create a local venv, if it does not exists.
   ```bash
   python -m venv .venv
   ```
  Activate the local env on terminal -> Windows - .\.venv\Scripts\Activate
4. Install the dependencies using the following command:

   ```bash
   pip install -r requirements.txt
   ```
## Usage
To execute the tests, follow the steps below:

Navigate to the project's root directory.

### Contract creator - Execute the following command:(Windows)
   ```bash
        pytest .tests\consumer\tests\
        or 
        pytest .tests\consumer\tests\test_{file_name}.py
   ```

### Contract creator - Execute the following command:(Linux)
   ```bash
        pytest ./tests/consumer/tests/
        # or
        pytest ./tests/consumer/tests/test_{file_name}.py
   ```

Note: Check the contracts created on ./broker/contracts/

### Check the contracts created on ./broker/contracts/(Windows)

   ```bash
        pytest .tests/provider/tests/
        # or
        pytest .tests/provider/tests/test_{file_name}.py
   ```

### Using Pact Broker (Docker)

#### Dependencies:
Note: The contracts created by consumer SHOULD exists OR you need to run the consumer tests to build the contracts.

#### How to run?

1 - Open a terminal and execute start the pactfoundation/pact-broker and postgres images
   ```bash
      docker-compose -f tests/broker/docker-compose.yml up
   ```
2 - Check if the PactBrocker is running
   - Open a browser and use this URL: http://localhost:9292
3 - Publish the contracts on PactBroker
   ```bash
      pact-broker publish tests/broker/contracts/countries --consumer-app-version=1.0.0 --broker-base-url=http://localhost:9292 --tag=dev
   ```
4 - Run the Verify to check the Pact: Doc: https://docs.pact.io/implementation_guides/python/docs/provider
   ```bash
      pact-verifier --provider-base-url="https://restcountries.com/v3.1" --provider-app-version="1.0.0" --pact-url=http://localhost:9292/pacts/provider/<provider-value-inside-the-contract>/consumer/<consumer-value-inside-the-contract>/latest --publish-verification-results --enable-pending
   ```
   or 
   Run the Verify to check all contracts
   ```bash
      pact-verifier --provider-base-url="https://restcountries.com/v3.1" --provider-app-version="1.0.0" --pact-broker-url=http://localhost:9292 --provider="provider" --publish-verification-results --enable-pending 
   ```

#### Using tags:
3 - Publish the contracts on PactBroker
   ```bash
      pact-broker publish tests/broker/contracts/<folder-with-the-pact-contracts> --consumer-app-version=1.0.1 --broker-base-url=http://localhost:9292 --tag=dev
   ```
4 - Run the Verify to check the Pact: Doc: https://docs.pact.io/implementation_guides/python/docs/provider
   ```bash
      pact-verifier --provider-base-url="https://restcountries.com/v3.1" --provider-app-version="1.0.1" --pact-url=http://localhost:9292/pacts/provider/<provider-value-inside-the-contract>/consumer/<consumer-value-inside-the-contract>/dev --publish-verification-results --enable-pending
   ```
   or 
   Run the Verify to check all contracts
   ```bash
      pact-verifier --provider-base-url="https://restcountries.com/v3.1" --provider-app-version="1.0.1" --pact-broker-url=http://localhost:9292 --provider="provider" --publish-verification-results --enable-pending --consumer-version-tag=dev --provider-version-tag=dev
   ```
CLI command documentation: https://docs.pact.io/implementation_guides/python/docs/provider



