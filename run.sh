#!/bin/bash

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Virtual environment not found. Run: make install"
    exit 1
fi

python main.py "$@"
