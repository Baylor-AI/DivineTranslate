#!/bin/bash

# Exit script
set -e

# Create rivas-venv (accounts for both Mac and Windows)
# python3 -m venv rivas-venv
echo "[START] Creating virtual environment rivas-venv..."

if python3_version=$(python3 --version 2>&1) && [[ $python3_version == *"Python 3"* ]]
then
    echo "[CHECK] Python 3 version found: $python3_version"
    python3 -m venv rivas-venv
    source rivas-venv/bin/activate
elif python_version=$(python --version 2>&1) && [[ $python_version == *"Python 3"* ]]
then
    echo "[CHECK] Python version found: $python_version"
    python -m venv rivas-venv
    source rivas-venv/Scripts/activate
else
    echo "[ERROR] No valid Python version found. Install or update to Python 3 before running this script again."
fi

echo "[DONE] Created and activated rivas-venv..."

# Check for npm
if ! command -v npm &> /dev/null
then
    echo "[ERROR] npm could not be found, please install it first."
    exit 1
fi

# Install requirements
pip install -r requirements.txt
npm install react-scripts --save
npm install bootstrap --save

echo ""
echo "[COMPLETED] Setup completed successfully..."

# run backend to test
# source rivas-venv/bin/activate
# uvicorn WordNetEndpoint:app --host 0.0.0.0 --port 8000 --reload