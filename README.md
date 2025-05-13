# Contract Test Framework

This project is a contract testing framework designed to validate interactions between a consumer and a provider using the Pact framework.

Helper: https://docs.pact.io/implementation_guides/python

---

## Folder Structure
contract-test-framework/
├── broker/                          # Acts as local Pact Broker
│   └── contracts/                   # Generated contract files
│       └── folders
│            └── consumer-provider.json   # Example contract
│
├── consumer/
│   ├── contracts/                   # Consumer contract definitions
│   │   ├── mock-data/               # Organized by endpoint
│   │   │   ├── countries/
│   │   │   │   └── brazil.json      # Example mock response
│   │
│   └── tests/
│       ├── contract_tests/          # Pact contract tests
│       │   └── test_country_api_builder_contract.py
│       └── unit/                    # Regular unit tests
│           └── test_helpers.py
│
├── provider/
│   └── tests/
│       │   └── verify_contracts.py
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
└── README.md                        # Project docs

# Notes and Considerations
'''
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

'''

