Write-Host "🔧 Creating virtual environment..."
python -m venv venv
if (-Not $?) {
    Write-Host "❌ Failed to create virtual environment"
    exit 1
}
Write-Host "✅ Virtual environment created."

Write-Host "📦 Installing dependencies..."
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✅ All dependencies installed."
