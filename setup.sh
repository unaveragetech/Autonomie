#!/bin/bash

# Instructions:
# This script sets up the Autonomie project environment on Linux or Windows.
# It installs pip, required Python libraries, and Tesseract OCR.
#
# Usage:
# - **For Linux**:
#   Run this script using: `bash setup.sh`
#   The script will execute the following commands:
#     1. Update package list: `sudo apt-get update`
#     2. Install pip: `sudo apt-get install -y python3-pip`
#     3. Install Python libraries: `pip install -r requirements.txt`
#     4. Install Tesseract OCR: `sudo apt-get install -y tesseract-ocr`
#     5. Add Tesseract to PATH (if needed):
#        ```
#        TESSERACT_DIR=$(dirname "$(command -v tesseract)")
#        echo "export PATH=\$PATH:$TESSERACT_DIR" >> ~/.bashrc
#        source ~/.bashrc
#        ```
#
# - **For Windows**:
#   Run this script using a Bash environment like Git Bash or WSL:
#     1. Install pip: `python -m ensurepip --upgrade`
#     2. Install Python libraries: `pip install -r requirements.txt`
#     3. Install Tesseract OCR manually if missing:
#        Download from: https://github.com/tesseract-ocr/tesseract
#        Ensure Tesseract is added to the system PATH during installation.
#
#   Alternatively, manually execute the commands printed by this script.

echo "Setting up the Autonomie environment..."

# Detect the operating system
OS_TYPE=$(uname -s)
echo "Detected OS: $OS_TYPE"

if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Running setup for Linux..."
    echo "Commands being executed:"
    echo "  1. sudo apt-get update"
    echo "  2. sudo apt-get install -y python3-pip"
    echo "  3. pip install -r requirements.txt"
    echo "  4. sudo apt-get install -y tesseract-ocr (if not installed)"
    echo "  5. Add Tesseract to PATH if necessary."

    # Update and install pip
    sudo apt-get update
    sudo apt-get install -y python3-pip

    # Install required Python libraries
    pip install -r requirements.txt

    # Install Tesseract OCR if not already installed
    if ! command -v tesseract &> /dev/null
    then
        sudo apt-get install -y tesseract-ocr
    fi

    # Verify Tesseract installation and add to PATH if necessary
    if ! echo "$PATH" | grep -q "$(dirname "$(command -v tesseract)")"; then
        TESSERACT_DIR=$(dirname "$(command -v tesseract)")
        echo "export PATH=\$PATH:$TESSERACT_DIR" >> ~/.bashrc
        export PATH=$PATH:$TESSERACT_DIR
        echo "Added Tesseract to PATH. Restart terminal or source ~/.bashrc to apply changes."
    fi

    echo "Linux setup complete!"

elif [[ "$OS_TYPE" == "MINGW"* || "$OS_TYPE" == "CYGWIN"* || "$OS_TYPE" == "MSYS"* ]]; then
    echo "Running setup for Windows..."
    echo "Commands to execute (if using manual steps):"
    echo "  1. python -m ensurepip --upgrade"
    echo "  2. pip install -r requirements.txt"
    echo "  3. Install Tesseract OCR manually if missing."
    echo "     Download Tesseract from: https://github.com/tesseract-ocr/tesseract"
    echo "     Ensure to add Tesseract to the system PATH."

    # Install pip
    python -m ensurepip --upgrade

    # Install required Python libraries
    pip install -r requirements.txt

    # Check for Tesseract OCR installation
    if ! where tesseract &> /dev/null
    then
        echo "Tesseract OCR is not installed. Please download and install Tesseract manually."
    fi

    echo "Windows setup complete!"

else
    echo "Unsupported operating system. Please run this script on Linux or Windows."
    exit 1
fi

echo "Setup complete!"
