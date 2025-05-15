. "$PSScriptRoot\common_setup.ps1"

Write-Host "🔹 [1/2] Running consumer tests to generate contracts..."
pytest .\consumer\tests\

Write-Host "🔹 [2/2] Running local Pact verifier against generated contracts..."
pytest .\provider\tests\

Write-Host "✅ Local broker workflow complete."