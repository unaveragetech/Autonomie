import threading
import time

class CLIInterface:
    def __init__(self, engine=None):
        """Initialize the CLI interface with an optional reference to the engine."""
        self.running = True
        self.paused = False
        self.logs = []
        self.commands = []
        self.engine = engine  # Optionally pass the engine for further control
        self.log("CLI initialized")

    def log(self, message):
        """Log a message to the CLI window."""
        self.logs.append(message)
        print(f"[CLI] {message}")

    def add_command(self, command):
        """Add a command to be processed."""
        self.commands.append(command)

    def start(self):
        """Start the CLI in a separate thread to accept user input."""
        thread = threading.Thread(target=self.run_cli)
        thread.daemon = True
        thread.start()

    def run_cli(self):
        """Main CLI loop to capture user input."""
        while self.running:
            command = input("> ").strip().lower()  # Normalize input for easier processing
            self.add_command(command)
            self.log(f"Command received: {command}")
            self.process_command(command)

    def process_command(self, command):
        """Process user commands."""
        if command == "exit":
            self.log("Shutting down...")
            self.running = False
            if self.engine:
                self.engine.stop()  # Optionally stop the engine if passed
        elif command == "help":
            self.display_help()
        elif command == "pause":
            self.paused = True
            self.log("Autonomie engine paused.")
            if self.engine:
                self.engine.pause()  # Pause the engine processing if applicable
        elif command == "resume":
            self.paused = False
            self.log("Autonomie engine resumed.")
            if self.engine:
                self.engine.resume()  # Resume the engine processing if applicable
        elif command == "toggle_logging":
            self.toggle_logging()
        elif command == "clear_logs":
            self.clear_logs()
        elif command == "status":
            self.show_status()
        else:
            self.log(f"Unknown command: {command}")
            self.display_help()

    def display_help(self):
        """Display available commands."""
        help_text = """
Available commands:
- exit: Shut down the Autonomie engine.
- help: Display this help message.
- pause: Pause the Autonomie engine.
- resume: Resume the Autonomie engine if paused.
- toggle_logging: Toggle the display of logs in the CLI.
- clear_logs: Clear the current log messages.
- status: Display the current status of the engine (running/paused).
"""
        self.log(help_text)

    def toggle_logging(self):
        """Toggle the logging of messages in the CLI."""
        if hasattr(self, 'logging_enabled'):
            self.logging_enabled = not self.logging_enabled
        else:
            self.logging_enabled = True
        status = "enabled" if self.logging_enabled else "disabled"
        self.log(f"Logging has been {status}.")

    def clear_logs(self):
        """Clear the logs."""
        self.logs = []
        self.log("Logs have been cleared.")

    def show_status(self):
        """Display the current status of the Autonomie engine."""
        if self.paused:
            self.log("Status: Autonomie engine is paused.")
        else:
            self.log("Status: Autonomie engine is running.")

# To integrate with the engine, the CLI would pass the engine as a parameter during initialization.
