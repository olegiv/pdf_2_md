@echo off
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Run: make install
    exit /b 1
)
python main.py %*
