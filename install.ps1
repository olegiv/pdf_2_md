Write-Host "🔧 Creating virtual environment..."
python -m venv venv
if (-Not $?) {
    Write-Host "❌ Failed to create virtual environment"
    exit 1
}
Write-Host "✅ Virtual environment created."

Write-Host "📦 Installing dependencies..."
.\\venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "📚 Downloading required NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

Write-Host "✅ All dependencies and NLTK data installed."
