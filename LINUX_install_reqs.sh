# Check python version
if python3_version=$(python3 --version 2>&1) && [[ $python3_version == *"Python 3"* ]]
then
    echo "[CHECK] Python 3 version found: $python3_version"
    python3 -m venv rivas-venv
    source rivas-venv/bin/activate
elif python_version=$(python --version 2>&1) && [[ $python_version == *"Python 3"* ]]
then
    # Shouldn't use this branch for Mac or Linux OS, but just in case user error
    echo ""
    echo "[ERROR] Detected Windows version of Python."
    echo "[SWITCHING] Switching to install for Windows, please wait..."
    sleep 5
    echo ""
    ./WIN_install_reqs.sh
    exit 1
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
# npm install react-scripts --save
# npm install bootstrap --save

echo ""
echo "[COMPLETED] Setup completed successfully..."
echo "[COMPLETED] rivas-venv has been created and requirements have been installed."
echo "To start the virtual environment:"
echo ""
echo "Start the virtual environment in this terminal:"
echo "source rivas-venv/bin/activate"
echo ""
echo "Then open a new terminal, navigate to the bible-frontend directory and run the commands below:"
echo "npm install react-scripts --save"
echo "npm install bootstrap --save"
echo ""
echo "After the install, you can start the frontend in this new terminal with:"
echo "npm start"
