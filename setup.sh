
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

# Check for Tesseract installation
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract OCR is not installed. Please install it from https://github.com/tesseract-ocr/tesseract"
else
    echo "Tesseract OCR is already installed."
fi

echo "Setup complete! Please ensure Tesseract is in your PATH."
