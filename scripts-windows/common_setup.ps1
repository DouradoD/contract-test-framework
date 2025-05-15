Write-Host " Starting the common setup ..."
Write-Host " [1/2] Creating virtual environment if it does not exist..."
if (!(Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host " [2/2] Installing Python requirements..."
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Check if pact-broker is installed, if not, install it
Write-Host " Checking if pact-broker CLI is installed..."
$pactBrokerCmd = Get-Command pact-broker -ErrorAction SilentlyContinue
if (-not $pactBrokerCmd) {
    Write-Host "pact-broker CLI not found. Installing pact_broker-client Ruby gem..."
    gem install pact_broker-client
    # After install, check again
    $pactBrokerCmd = Get-Command pact-broker -ErrorAction SilentlyContinue
    if ($pactBrokerCmd) {
        Write-Host "pact-broker CLI installed successfully."
    } else {
        Write-Host "pact-broker CLI installation failed. Please check your Ruby installation and PATH."
        exit 1
    }
} else {
    Write-Host "pact-broker CLI is already installed."
}