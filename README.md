Here's a revised and more detailed version of the README.md for your **Autonomie** project, including comprehensive setup instructions and a `setup.sh` script to automate the installation process. 

### README.md

```markdown
# Autonomie - User Interaction Engine

## Overview
Autonomie is a Python-based project designed to observe and learn from user activity on the screen. The engine captures and recognizes various objects and text using OpenCV and Tesseract, allowing it to remember and interact with UI elements across multiple sessions. This capability makes Autonomie a useful tool for automating repetitive tasks based on user behavior.

## Features
- **Object Recognition**: Automatically detects UI elements such as buttons, labels, icons, and more.
- **Text Recognition**: Utilizes Optical Character Recognition (OCR) to extract text from recognized screen elements.
- **Memory Persistence**: Remembers recognized objects across sessions, assigning unique IDs to recurring elements.
- **Interactive CLI Interface**: A command-line interface that logs actions and allows users to control the engine's behavior.

## Installation
To set up Autonomie, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/autonomie.git
   cd autonomie
   ```

2. **Run the Setup Script**:
   Execute the `setup.sh` script to install the necessary dependencies. This script handles library installations and prepares the environment.
   ```bash
   bash setup.sh
   ```

3. **Install Tesseract OCR**:
   Ensure that Tesseract OCR is installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract). Follow the instructions on that page for your specific operating system to install Tesseract.

4. **Add Tesseract to Your PATH**:
   After installation, make sure the Tesseract executable is available in your system's PATH. The method to do this varies by OS:
   - **Windows**: Modify the PATH environment variable in System Properties.
   - **Linux/Mac**: Add the Tesseract installation path to your `.bashrc` or `.bash_profile`:
     ```bash
     export PATH=$PATH:/path/to/tesseract
     ```

## Usage
Once the setup is complete, you can run the main script to start the Autonomie engine:
```bash
python main.py
```

### Available CLI Commands
- `exit`: Stops the engine and exits the program.
- `help`: Displays available commands and their descriptions.

## Contributing
Feel free to submit issues, suggest features, or contribute code. If you have any ideas or enhancements, please create a pull request!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### `setup.sh`

Here’s a sample `setup.sh` script that automates the installation of the required Python libraries:

```bash
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
```

### Instructions for Using `setup.sh`
1. Save the above script as `setup.sh` in the root of your `autonomie` project directory.
2. Make the script executable:
   ```bash
   chmod +x setup.sh
   ```
3. Run the script:
   ```bash
   ./setup.sh
   ```

### Final Note
With these changes, your README.md provides clear guidance on setting up the Autonomie engine, and the `setup.sh` script automates most of the setup process. Let me know if you need any further modifications or additions!
