$env:API_HUB_BROKER_BASE_URL = "https://<your-url>.pactflow.io"
$env:API_HUB_BROKER_TOKEN = "<your-token>"

. "$PSScriptRoot\common_setup.ps1"

Write-Host " [1/2] Running consumer tests to publish contracts to API Hub..."
pact-broker publish ./broker/contracts/countries `
  --consumer-app-version=1.0.1 `
  --broker-base-url=$env:API_HUB_BROKER_BASE_URL `
  --broker-token=$env:API_HUB_BROKER_TOKEN `
  --tag=dev

if ($LASTEXITCODE -ne 0) {
    Write-Host "pact-broker publish failed."
    exit $LASTEXITCODE
}

Write-Host " [2/2] Running provider verification against contracts from API Hub..."
pact-verifier `
  --provider-base-url=https://restcountries.com/v3.1 `
  --pact-broker-url=$env:API_HUB_BROKER_BASE_URL `
  --pact-broker-token=$env:API_HUB_BROKER_TOKEN `
  --provider-app-version="1.0.1" `
  --provider="provider-restcountries" `
  --publish-verification-results `
  --enable-pending

if ($LASTEXITCODE -ne 0) {
    Write-Host "pact-verifier failed."
    exit $LASTEXITCODE
}

Write-Host "API Hub workflow complete."