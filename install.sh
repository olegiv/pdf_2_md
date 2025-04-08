#!/bin/bash

echo "🔧 Creating virtual environment..."
python -m venv venv || { echo '❌ Failed to create virtual environment'; exit 1; }

echo "✅ Virtual environment created."

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ All dependencies installed."
