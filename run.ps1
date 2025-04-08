if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Run: make install"
    exit 1
}
python main.py $args
