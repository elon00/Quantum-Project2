# Hybrid Handshake Setup Script (Windows)
# Run: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== PQC Hybrid Handshake Setup ===" -ForegroundColor Cyan

# Install dependencies via winget
$packages = @(
    "Python.Python.3.12",
    "Git.Git",
    "Kitware.CMake",
    "Microsoft.VisualStudio.2022.BuildTools"
)

foreach ($pkg in $packages) {
    Write-Host "Checking $pkg..."
    winget install $pkg --accept-package-agreements --accept-source-agreements 2>$null
}

# Refresh PATH
$pythonPath = "$env:LOCALAPPDATA\Programs\Python\Python312"
$pythonScripts = "$pythonPath\Scripts"
$gitPath = "C:\Program Files\Git\cmd"
$cmakePath = "C:\Program Files\CMake\bin"
$env:PATH = "$pythonPath;$pythonScripts;$gitPath;$cmakePath;$env:PATH"

Write-Host "`nVerifying tools..."
python --version
git --version
cmake --version

Write-Host "`nInstalling Python packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "`nTesting liboqs (first import may take several minutes)..."
python -c "import oqs; print('liboqs OK'); kems = oqs.get_enabled_KEM_mechanisms(); print(f'KEMs available: {len(kems)}'); print('Kyber768' if 'Kyber768' in kems else 'WARNING: Kyber768 not found')"

Write-Host "`n=== Setup complete ===" -ForegroundColor Green
Write-Host "Run server:  python server.py"
Write-Host "Run client:  python client.py"
