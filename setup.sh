#!/bin/bash

# Setup script for Autonomie project

echo "Setting up the Autonomie environment..."

# Update and install pip
echo "Updating package list and installing pip..."
sudo apt-get update
sudo apt-get install -y python3-pip

# Install required Python libraries
echo "Installing required Python libraries from requirements.txt..."
pip install -r requirements.txt

# Install Tesseract OCR if not already installed
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract OCR is not installed. Installing Tesseract..."
    sudo apt-get install -y tesseract-ocr
else
    echo "Tesseract OCR is already installed."
fi

# Verify Tesseract installation and add to PATH if necessary
if ! echo "$PATH" | grep -q "$(dirname "$(command -v tesseract)")"; then
    echo "Adding Tesseract to the PATH..."
    TESSERACT_DIR=$(dirname "$(command -v tesseract)")
    echo "export PATH=\$PATH:$TESSERACT_DIR" >> ~/.bashrc
    export PATH=$PATH:$TESSERACT_DIR
    echo "Tesseract has been added to the PATH. Restart your terminal or source ~/.bashrc to update."
fi

echo "Setup complete! Tesseract OCR is installed and available in the PATH."
