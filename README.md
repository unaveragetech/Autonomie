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
   git clone https://github.com/unaveragetech/autonomie.git
   cd autonomie
   ```

2. **Run the Setup Script**:
   Execute the `setup.sh` script to install the necessary dependencies. This script handles library installations and prepares the environment.
   ```bash
   bash setup.sh
   ```

3. **Install Tesseract OCR**:
   Ensure that Tesseract OCR is installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract). Follow the instructions on that page for your specific operating system to install Tesseract.
 [Download tesseract-ocr.mirror here ](https://sourceforge.net/projects/tesseract-ocr.mirror/)
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
```
### Available CLI Commands

- `exit`: Stops the engine and exits the program gracefully. This command will end both the CLI and the Autonomie engine.
- `help`: Displays a list of all available commands and their descriptions for user guidance.
- `pause`: Temporarily pauses the Autonomie engine, stopping it from processing screen data. Use this when you want to halt the engine without exiting.
- `resume`: Resumes the Autonomie engine if it has been paused, allowing it to continue processing screen data.
- `toggle_logging`: Toggles the logging feature on or off. When logging is disabled, the engine's actions will no longer be printed to the CLI.
- `clear_logs`: Clears the current logs from the CLI display. Useful if you want to remove clutter and start with a clean log window.
- `status`: Displays the current status of the Autonomie engine, indicating whether it is running or paused.
```

```
## Contributing
Feel free to submit issues, suggest features, or contribute code. If you have any ideas or enhancements, please create a pull request!
```
```
## License
This project is licensed under the sduc License - see the [LICENSE](LICENSE) file for details.
```


