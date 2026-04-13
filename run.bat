@echo off
echo Starting Ollama...
start /B ollama serve

echo Waiting for Ollama to start...
timeout /t 5

echo Starting AI Excuse Generator...
python app.py

pause