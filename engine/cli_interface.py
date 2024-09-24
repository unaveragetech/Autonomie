import threading
import time

class CLIInterface:
    def __init__(self):
        self.running = True
        self.logs = []
        self.commands = []
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
            command = input("> ")
            self.add_command(command)
            self.log(f"Command received: {command}")
            self.process_command(command)

    def process_command(self, command):
        """Process user commands."""
        if command == "exit":
            self.log("Shutting down...")
            self.running = False
        elif command == "help":
            self.log("Available commands: exit, help")
        else:
            self.log(f"Unknown command: {command}")
