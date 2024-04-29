# Check python version
if python3_version=$(python3 --version 2>&1) && [[ $python3_version == *"Python 3"* ]]
then
    # Shouldn't use this branch for Windows OS, but just in case user error
    echo ""
    echo "[ERROR] Detected Mac or Linus version of Python."
    echo "[SWITCHING] Switching to install for Mac or Linux, please wait..."
    sleep 5
    echo ""
    ./LINUX_install_reqs.sh
    exit 1
elif python_version=$(python --version 2>&1) && [[ $python_version == *"Python 3"* ]]
then
    # echo "[INSTALL] Installing react-scripts and boostrap..."
    # powershell -ExecutionPolicy Bypass -File "./WIN_installreqs.ps1"
    # echo "[COMPLETE] Installed react-scripts and boostrap."
    # echo ""
    echo "[CHECK] Python version found: $python_version"
    python -m venv rivas-venv
    source rivas-venv/Scripts/activate
else
    echo "[ERROR] No valid Python version found. Install or update to Python 3 before running this script again."
fi

echo "[DONE] Created and activated rivas-venv..."

# # Check for npm
# if ! command -v npm &> /dev/null
# then
#     echo "[ERROR] npm could not be found, please install it first."
#     exit 1
# fi

# Install requirements
echo "[INSTALL] Installing requirements.txt..."
pip install -r requirements.txt
echo "[COMPLETE] Installed requirements.txt"

echo ""
echo "[COMPLETED] Setup completed successfully..."
echo "[COMPLETED] rivas-venv has been created and requirements have been installed."
echo "_____________________________"
echo "NEXT STEPS:"
echo ""
echo "Start the virtual environment in this terminal:"
echo "source rivas-venv/Scripts/activate"
echo ""
echo "Then you will be able to start the backend server"
echo ""
echo "Then open a new Powershell terminal, navigate to the bible-frontend directory and run the commands below:"
echo "npm install react-scripts --save"
echo "npm install bootstrap --save"
echo ""
echo "After the install has completed, you can start the frontend in this new terminal with:"
echo "npm start"
