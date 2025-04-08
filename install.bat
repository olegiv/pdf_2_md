@echo off
echo 🔧 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    exit /b 1
)
echo ✅ Virtual environment created.

echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ All dependencies installed.
