from engine.object_recognition import ObjectRecognitionEngine
from engine.cli_interface import CLIInterface
import time

def main():
    # Initialize the CLI interface and object recognition engine
    engine = ObjectRecognitionEngine()  # Initialize the engine first
    cli = CLIInterface(engine)  # Pass the engine to the CLI for control

    # Start CLI loop in a separate thread
    cli.start()

    try:
        # Main loop: process screen and listen to CLI commands
        while cli.running:  # Keep running as long as CLI is not stopped
            if not cli.paused:  # Only process screen if the engine is not paused
                engine.process_screen()  # Process screen and recognize objects
            else:
                time.sleep(0.1)  # Avoid busy-waiting when paused

    except KeyboardInterrupt:
        cli.log("KeyboardInterrupt received. Shutting down...")
    finally:
        cli.log("Stopping the engine...")
        engine.stop()  # Ensure engine cleanup if necessary
        cli.log("Autonomie engine stopped.")

if __name__ == "__main__":
    main()
