#!/bin/bash

# Exit script
set -e

# Create rivas-venv
python3 -m venv rivas-venv
source rivas-venv/bin/activate
echo "Created and activated rivas-venv..."

# Check for npm
if ! command -v npm &> /dev/null
then
    echo "npm could not be found, please install it first."
    exit 1
fi

# Install requirements
pip install -r requirements.txt
npm install react-scripts --save
npm install bootstrap --save

echo "Setup completed successfully..."

# run backend to test
# source rivas-venv/bin/activate
# uvicorn WordNetEndpoint:app --host 0.0.0.0 --port 8000 --reload