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

# Check the current path length and warn if it's too long
echo "[CHECKING] Checking length of file path..."
current_path=$(pwd)
path_length=${#current_path}
max_path_length=260

# echo "Enabling long paths..."
#pwsh
# pwsh Start-Process powershell -Verb runAs New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
# echo "[SUCCESS] Long paths enabled"


# if [ $path_length -ge $max_path_length ]; then
    
#     echo "[WARNING] The current path length is $path_length characters."
#     echo "This might cause problems with path length limitations in Windows."
#     echo "Consider moving your project to a shorter path, such as C:/Projects/"
#     echo "Alternatively, you can enable long path support in Windows 10/11:"
#     echo "1. Press Win + R, type 'regedit', and press Enter."
#     echo "2. Navigate to: Computer\\HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem"
#     echo "3. Right-click on 'FileSystem', select New -> DWORD (32-bit) Value, name it 'LongPathsEnabled'."
#     echo "4. Set the value of 'LongPathsEnabled' to 1."
#     echo "5. Restart your computer."
#     exit 1
# fi
# echo "[SUCCESS] File path length is acceptable, proceeding with install"

# Install requirements
echo "[INSTALL] Installing requirements.txt..."
pip install -r requirements.txt
echo "[COMPLETE] Installed requirements.txt"

echo "[INSTALL] Installing react-scripts and boostrap..."
powershell ./WIN_installreqs.ps1
echo "[COMPLETE] Installed react-scripts and boostrap."

# echo "[INSTALL] Installing react-scripts..."
# npm install react-scripts --save
# echo "[COMPLETE] Installed react-scripts"

# echo "[INSTALL] Installing boostrap..."
# npm install bootstrap --save
# echo "[COMPLETE] Installed boostrap"

echo ""
echo "[COMPLETED] Setup completed successfully..."
echo "[COMPLETED] rivas-venv has been created and requirements have been installed."
echo "To start the virtual environment:"
echo "source rivas-venv/Scripts/activate"
echo ""
