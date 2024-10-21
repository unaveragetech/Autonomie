import subprocess
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel
from pynput import keyboard, mouse
import time
import json
import os
import csv
import logging
from PIL import ImageGrab

# Set up logging
logging.basicConfig(filename='user_emulator.log', level=logging.DEBUG)

# Function to check and install a package
def install_package(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Check for required packages and install if not present
try:
    from PIL import ImageGrab
except ImportError:
    install_package('Pillow')
    from PIL import ImageGrab

# Recorder Class
class Recorder:
    def __init__(self):
        self.actions = []
        self.mouse_listener = None
        self.keyboard_listener = None
        self.hold_keys = set()  # Track currently held keys
        self.screenshot_dir = "screenshots"  # Directory for screenshots
        self.screenshot_enabled = False  # Toggle for screenshot capturing
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def record_action(self, event_type, details, category=None):
        timestamp = time.time()
        self.actions.append((event_type, details, timestamp, category))
        if self.screenshot_enabled:
            self.capture_screenshot(event_type, details)  # Capture screenshot if enabled

    def start_recording(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def on_click(self, x, y, button, pressed):
        category = simpledialog.askstring("Category", "Enter action category:")
        action = ('mouse_click', (x, y, button.name, pressed))
        self.record_action(*action, category)
        self.show_action_popup(f"Mouse Click: {button.name} at ({x}, {y}) - {'Pressed' if pressed else 'Released'}")

    def on_move(self, x, y):
        category = simpledialog.askstring("Category", "Enter action category:")
        action = ('mouse_move', (x, y))
        self.record_action(*action, category)
        self.show_action_popup(f"Mouse Moved to: ({x}, {y})")

    def on_scroll(self, x, y, dx, dy):
        category = simpledialog.askstring("Category", "Enter action category:")
        action = ('mouse_scroll', (x, y, dx, dy))
        self.record_action(*action, category)
        self.show_action_popup(f"Mouse Scroll at: ({x}, {y}), delta: ({dx}, {dy})")

    def on_press(self, key):
        category = simpledialog.askstring("Category", "Enter action category:")
        if hasattr(key, 'char') and key.char:
            action = ('key_press', str(key.char))
        else:
            action = ('key_press', str(key))  # Handle special keys
        self.record_action(*action, category)
        self.hold_keys.add(key)  # Track held keys
        self.show_action_popup(f"Key Pressed: {str(key)}")

    def on_release(self, key):
        category = simpledialog.askstring("Category", "Enter action category:")
        action = ('key_release', str(key))
        self.record_action(*action, category)
        self.hold_keys.discard(key)  # Remove from held keys
        self.show_action_popup(f"Key Released: {str(key)}")

    def capture_screenshot(self, event_type, details):
        """ Capture a screenshot of the full screen or an area around the mouse depending on the event. """
        screenshot_file = f"{self.screenshot_dir}/screenshot_{event_type}_{int(time.time())}.png"
        if event_type == 'mouse_move' or event_type == 'mouse_click':
            x, y = details[:2]
            screenshot_area = (x - 50, y - 50, x + 50, y + 50)  # Capture area around the mouse
            screenshot = ImageGrab.grab(bbox=screenshot_area)
        else:
            screenshot = ImageGrab.grab()  # Full screen capture
        screenshot.save(screenshot_file)
        logging.info(f'Screenshot saved: {screenshot_file}')

    def get_actions(self):
        return self.actions

    def clear_actions(self):
        self.actions = []

    def toggle_screenshots(self):
        self.screenshot_enabled = not self.screenshot_enabled
        return self.screenshot_enabled

    def show_action_popup(self, message):
        if not hasattr(self, 'popup'):
            self.popup = Toplevel()
            self.popup.title("Recording Actions")
            self.popup.geometry("300x200")
            self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

            self.text_area = tk.Text(self.popup)
            self.text_area.pack(expand=True, fill='both')

            self.close_button = tk.Button(self.popup, text="Stop Recording", command=self.close_popup)
            self.close_button.pack(pady=10)

        self.text_area.insert(tk.END, message + '\n')
        self.text_area.see(tk.END)  # Auto-scroll to the bottom

    def close_popup(self):
        self.popup.destroy()
        del self.popup  # Allow for a new popup to be created

# Player Class
class Player:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def playback(self, actions):
        for action in actions:
            event_type, details, _timestamp, _category = action
            if event_type == 'mouse_click':
                x, y, button, pressed = details
                self.mouse_controller.position = (x, y)
                if pressed:
                    self.mouse_controller.click(button)
            elif event_type == 'mouse_move':
                x, y = details
                self.mouse_controller.position = (x, y)
            elif event_type == 'mouse_scroll':
                x, y, dx, dy = details
                self.mouse_controller.position = (x, y)
                self.mouse_controller.scroll(dx, dy)
            elif event_type == 'key_press':
                self.keyboard_controller.press(details)
            elif event_type == 'key_release':
                self.keyboard_controller.release(details)

# TaskManager Class
class TaskManager:
    @staticmethod
    def save_task(actions, filename):
        with open(filename, 'w') as f:
            json.dump(actions, f)

    @staticmethod
    def load_task(filename):
        with open(filename, 'r') as f:
            actions = json.load(f)
        return actions

    @staticmethod
    def export_to_csv(actions, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Event Type', 'Details', 'Timestamp', 'Category'])
            for action in actions:
                writer.writerow(action)

    @staticmethod
    def import_from_csv(filename):
        actions = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                event_type = row[0]
                details = json.loads(row[1])  # Assuming details are JSON encoded
                timestamp = float(row[2])
                category = row[3]
                actions.append((event_type, details, timestamp, category))
        return actions

# GUI Class with Keybinds and Status Bar
class UserEmulatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("User Emulator")

        self.recorder = Recorder()
        self.player = Player()
        self.task_manager = TaskManager()

        self.create_widgets()
        self.create_keybindings()
        self.update_status()

    def create_widgets(self):
        self.record_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.record_button.pack()

        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        self.save_button = tk.Button(self.master, text="Save Task", command=self.save_task)
        self.save_button.pack()

        self.load_button = tk.Button(self.master, text="Load Task", command=self.load_task)
        self.load_button.pack()

        self.export_button = tk.Button(self.master, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack()

        self.import_button = tk.Button(self.master, text="Import from CSV", command=self.import_from_csv)
        self.import_button.pack()

        self.toggle_screenshot_button = tk.Button(self.master, text="Toggle Screenshots", command=self.toggle_screenshots)
        self.toggle_screenshot_button.pack()

        self.playback_button = tk.Button(self.master, text="Playback Task", command=self.playback_task)
        self.playback_button.pack()

        self.status_bar = tk.Label(self.master, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_keybindings(self):
        self.master.bind("<Control-r>", lambda event: self.start_recording())
        self.master.bind("<Control-s>", lambda event: self.stop_recording())
        self.master.bind("<Control-p>", lambda event: self.playback_task())

    def update_status(self, status_text="Ready"):
        self.status_bar.config(text=f"Status: {status_text}")

    def start_recording(self):
        self.recorder.start_recording()
        self.update_status("Recording...")

    def stop_recording(self):
        self.recorder.stop_recording()
        self.update_status("Stopped")

    def save_task(self):
        filename = simpledialog.askstring("Save Task", "Enter filename:")
        if filename:
            self.task_manager.save_task(self.recorder.get_actions(), filename + ".json")
            self.update_status(f"Task saved as {filename}.json")

    def load_task(self):
        filename = simpledialog.askstring("Load Task", "Enter filename:")
        if filename:
            actions = self.task_manager.load_task(filename + ".json")
            self.recorder.clear_actions()
            self.recorder.actions = actions
            self.update_status(f"Task loaded from {filename}.json")

    def export_to_csv(self):
        filename = simpledialog.askstring("Export to CSV", "Enter filename:")
        if filename:
            self.task_manager.export_to_csv(self.recorder.get_actions(), filename + ".csv")
            self.update_status(f"Task exported as {filename}.csv")

    def import_from_csv(self):
        filename = simpledialog.askstring("Import from CSV", "Enter filename:")
        if filename:
            actions = self.task_manager.import_from_csv(filename + ".csv")
            self.recorder.clear_actions()
            self.recorder.actions = actions
            self.update_status(f"Task imported from {filename}.csv")

    def playback_task(self):
        self.player.playback(self.recorder.get_actions())
        self.update_status("Playing back...")

    def toggle_screenshots(self):
        is_enabled = self.recorder.toggle_screenshots()
        status = "enabled" if is_enabled else "disabled"
        self.update_status(f"Screenshots {status}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = UserEmulatorGUI(root)
    root.mainloop()
