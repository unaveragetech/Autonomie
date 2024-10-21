import subprocess
import os
import logging
import sys
import time
import signal
import tkinter as tk  # Assuming you are using tkinter for the GUI
from tkinter import messagebox  # To show messages in the GUI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def stop_existing_xvfb(display_number):
    """Stop any existing Xvfb server running on the specified display."""
    try:
        # Find the process ID (PID) of the Xvfb server
        pid = subprocess.check_output(["pgrep", "-f", f"Xvfb :{display_number}"]).strip()
        if pid:
            logging.info(f"Stopping existing Xvfb server with PID {pid.decode()} on display {display_number}.")
            os.kill(int(pid), signal.SIGTERM)  # Terminate the Xvfb process
            time.sleep(2)  # Wait for a moment to ensure it terminates
    except subprocess.CalledProcessError:
        logging.info(f"No existing Xvfb server found on display {display_number}.")

def create_xauthority():
    """Create .Xauthority file if it doesn't exist."""
    xauthority_path = os.path.expanduser("~/.Xauthority")
    if not os.path.exists(xauthority_path):
        open(xauthority_path, 'a').close()
        logging.info(f"Created .Xauthority file at {xauthority_path}.")
    else:
        logging.info(f".Xauthority file already exists at {xauthority_path}.")
    
    os.environ["XAUTHORITY"] = xauthority_path  # Set XAUTHORITY

def start_xvfb():
    """Start Xvfb and set DISPLAY variable."""
    display_number = "99"  # No need for colon here, added in the call later
    stop_existing_xvfb(display_number)  # Stop any existing Xvfb server
    
    # Create .Xauthority file
    create_xauthority()

    # Start Xvfb
    logging.info("Starting Xvfb...")
    xvfb_command = ["Xvfb", f":{display_number}", "-screen", "0", "1024x768x24", "-nolisten", "tcp"]

    # Run the command in the background
    xvfb_process = subprocess.Popen(xvfb_command)
    time.sleep(2)  # Wait a moment for Xvfb to start
    
    # Set DISPLAY environment variable
    os.environ["DISPLAY"] = f":{display_number}"
    logging.info(f"Xvfb started on :{display_number}.")

    return xvfb_process

class UserEmulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("User Emulator")

        # Example widgets
        self.label = tk.Label(master, text="Welcome to the User Emulator!")
        self.label.pack()

        self.run_button = tk.Button(master, text="Run Main Application", command=self.run_main_application)
        self.run_button.pack()

    def run_main_application(self):
        """Method to run the main application logic."""
        try:
            import main2  # Ensure main2.py is in the same directory or in PYTHONPATH
            main2.main()  # Call the main function in main2.py
            messagebox.showinfo("Success", "Main application ran successfully.")
        except Exception as e:
            logging.error("An error occurred while running the main application.", exc_info=True)
            messagebox.showerror("Error", "An error occurred. Check the logs for more details.")

def main():
    logging.info("Starting the application...")

    # Start the Xvfb display
    xvfb_process = start_xvfb()

    # Start the GUI
    root = tk.Tk()
    emulator_gui = UserEmulatorGUI(root)

    try:
        root.mainloop()  # Start the Tkinter event loop
    except Exception as e:
        logging.error("An error occurred in the GUI.", exc_info=True)
    finally:
        # Terminate Xvfb process
        logging.info("Terminating Xvfb...")
        xvfb_process.terminate()
        xvfb_process.wait()  # Ensure the process has terminated
        logging.info("Xvfb terminated.")

# Main execution
if __name__ == "__main__":
    main()
