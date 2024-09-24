from engine.object_recognition import ObjectRecognitionEngine
from engine.cli_interface import CLIInterface

def main():
    # Initialize the CLI interface and object recognition engine
    cli = CLIInterface()
    engine = ObjectRecognitionEngine(cli)

    # Start CLI loop in a separate thread
    cli.start()

    # Start processing the screen and recognizing objects
    while True:
        engine.process_screen()

if __name__ == "__main__":
    main()
