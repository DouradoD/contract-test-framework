# Contract Test Framework

This project is a contract testing framework designed to validate interactions between a consumer and a provider using the Pact framework.

Helper: https://docs.pact.io/implementation_guides/python

---

## Folder Structure
contract-test-framework/
├── broker/                          # Acts as local Pact Broker
│   ├── contracts/                   # Generated contract files
│   │   └── consumer-provider.json   # Example contract
│   └── latest/                      # Symlinks for versioning (optional)
│
├── consumer/
│   ├── contracts/                   # Consumer contract definitions
│   │   ├── mock-data/               # Organized by endpoint
│   │   │   ├── countries/
│   │   │   │   └── brazil.json      # Example mock response
│   │   └── schemas/                 # JSON schemas for validation
│   │       └── country-schema.json
│   │
│   └── tests/
│       ├── contract_tests/          # Pact contract tests
│       │   └── test_country_api.py
│       └── unit/                    # Regular unit tests
│           └── test_helpers.py
│
├── provider/
│   ├── services/                    # Provider service code
│   │   └── country_service.py
│   │
│   └── tests/
│       ├── contract_verification/   # Pact verification tests
│       │   └── verify_contracts.py
│       └── integration/             # Regular integration tests
│           └── test_country_api.py
│
├── .vscode/
│   └── launch.json                  # Debug configs
│
├── config/
│   ├── pact-config.yml              # Pact CLI configuration
│   └── test-config.yml              # Environment configs
│
├── scripts/
│   ├── publish_contracts.sh         # CI scripts
│   └── verify_contracts.sh
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Pact test environment
├── docker-compose.yml               # Service definitions
└── README.md                        # Project docs
