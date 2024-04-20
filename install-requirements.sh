#!/bin/bash

# Prompt the user for input
echo "[CHECK OS] Are you on Windows? (y/n)"
read response

# Check the user input
if [[ $response == "y" ]] || [[ $response == "Y" ]]; then
    echo "[START] Creating virtual environment rivas-venv..."
    echo "[WINDOWS] Confirmed on Windows OS"
    ./WIN_install_reqs.sh
elif [[ $response == "n" ]] || [[ $response == "N" ]]; then
    echo "[START] Creating virtual environment rivas-venv..."
    echo "[LINUX] Confirmed on Mac OS or Linux OS"
    ./LINUX_install_reqs.sh
else
    echo "[ERROR] Invalid response, exiting..."
    exit 1
fi

