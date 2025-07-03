@echo off
REM Simple script to set up a virtual environment and start the API
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
