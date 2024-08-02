@echo off
rem Start the uvicorn server
start "" "http://localhost:23335"
uvicorn main:app --reload --port 23335

rem Deactivate the virtual environment after the server stops
deactivate