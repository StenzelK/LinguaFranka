@echo off
setlocal EnableDelayedExpansion

:: Check for Python installation
echo Checking for Python installation...
python --version >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...

    :: Install Python
    start /wait python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Confirm Python installation
    echo Verifying Python installation...
    python --version >nul 2>&1

    if %ERRORLEVEL% NEQ 0 (
        echo Python installation failed. Please install Python manually.
        exit /b 1
    ) else (
        echo Python installed successfully.
    )
) else (
    echo Python is already installed.
)

:: Install pip requirements
if exist requirements.txt (
    echo Installing pip requirements...
    pip install -r requirements.txt

    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip requirements.
        exit /b 1
    ) else (
        echo Pip requirements installed successfully.
    )
) else (
    echo requirements.txt not found. Skipping pip requirements installation.
)

echo Installation complete.
exit /b 0