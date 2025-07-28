import subprocess
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, scrolledtext
from pynput import keyboard, mouse
import time
import json
import os
import csv
import logging
import requests
import pytesseract
import base64
from PIL import Image, ImageGrab
from typing import List, Dict, Optional, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import platform
import pygetwindow as gw  # For window tracking

# Configuration constants
DEFAULT_MODELS = {
    "chat": "llama3",
    "vision": "llava",
    "analysis": "mixtral"
}
OLLAMA_BASE_URL = "http://localhost:11434/v1"  # Using OpenAI-compatible endpoint
SCREENSHOT_DIR = "screenshots"
CONFIG_FILE = "autonomie_config.json"
LOG_FILE = "user_emulator.log"

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OllamaManager:
    """Enhanced Ollama API handler with model management and retry logic."""
    def __init__(self):
        self.available_models = self._get_available_models()
        self._verify_model_availability()
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": "Bearer ollama"  # Ollama doesn't require auth but follows OpenAI format
        })

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _api_call(self, endpoint: str, payload: Dict) -> Dict:
        url = f"{OLLAMA_BASE_URL}{endpoint}"
        try:
            response = self.session.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API call failed: {str(e)}")
            raise

    def _get_available_models(self) -> List[str]:
        """Retrieve list of locally available Ollama models."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            response.raise_for_status()
            return [model["name"] for model in response.json().get("models", [])]
        except Exception as e:
            logging.error(f"Failed to get available models: {str(e)}")
            return []

    def _verify_model_availability(self):
        """Ensure required models are available."""
        for model_type, model_name in DEFAULT_MODELS.items():
            if model_name not in self.available_models:
                logging.warning(f"Model {model_name} not found. Attempting to pull...")
                try:
                    subprocess.run(["ollama", "pull", model_name], check=True)
                    self.available_models.append(model_name)
                except subprocess.CalledProcessError:
                    logging.error(f"Failed to download model {model_name}")
                    raise RuntimeError(f"Required model {model_name} not available")

    def chat_completion(self, messages: List[Dict[str, str]], model: str = DEFAULT_MODELS["chat"]) -> str:
        """Improved chat completion with proper OpenAI-compatible format."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "stream": False
        }
        response = self._api_call("/chat/completions", payload)
        return response["choices"][0]["message"]["content"]

    def vision_analysis(self, image_paths: List[str], prompt: str) -> str:
        """Perform multimodal analysis using vision model."""
        content = [{"type": "text", "text": prompt}]
        for path in image_paths:
            try:
                with open(path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                })
            except Exception as e:
                logging.warning(f"Image load failed for {path}: {str(e)}")
        payload = {
            "model": DEFAULT_MODELS["vision"],
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.5,
            "max_tokens": 1000
        }
        response = self._api_call("/chat/completions", payload)
        return response["choices"][0]["message"]["content"]

class ContextTracker:
    """Advanced context tracking for application and window states."""
    def __init__(self):
        self.current_application = None
        self.active_window = None
        self.last_interaction = None
        self.platform = platform.system()

    def update_context(self):
        try:
            if self.platform == "Windows":
                active_window = gw.getActiveWindow()
                self.active_window = active_window.title if active_window else "Unknown"
                self.current_application = active_window.owner if active_window else "Unknown"
            else:
                # Implement macOS/Linux specific tracking if needed
                self.active_window = "Unsupported Platform"
                self.current_application = "Unsupported Platform"
        except Exception as e:
            logging.warning(f"Window tracking failed: {str(e)}")
            self.active_window = "Error"
            self.current_application = "Error"

        self.last_interaction = time.time()

class EnhancedRecorder:
    """Improved recorder with event timing and contextual capture."""
    def __init__(self):
        self.actions = []
        self.listeners = []
        self.screenshot_dir = SCREENSHOT_DIR
        self._init_directories()
        self.ollama = OllamaManager()
        self.context = ContextTracker()

    def _init_directories(self):
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def start_recording(self):
        """Start listening for input events with precise timing."""
        self.listeners = [
            mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll),
            keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        ]
        for listener in self.listeners:
            listener.start()

    def stop_recording(self):
        """Stop all input listeners."""
        for listener in self.listeners:
            if listener.is_alive():
                listener.stop()

    def record_event(self, event_type: str, details: Dict, category: str = None):
        """Record an event with full contextual information."""
        self.context.update_context()
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "details": details,
            "category": category,
            "context": {
                "application": self.context.current_application,
                "window": self.context.active_window,
                "time_since_last": time.time() - self.context.last_interaction if self.context.last_interaction else 0
            }
        }
        self.actions.append(event)
        self._analyze_event(event)

    def _analyze_event(self, event: Dict):
        """Perform real-time analysis of captured events."""
        screenshot_path = self._capture_screenshot(event)
        if event["type"] == "text_input":
            analysis = self.ollama.chat_completion([{
                "role": "user",
                "content": f"Analyze this user input: {event['details']['text']}. "
                           "Provide sentiment and potential intent."
            }])
            event["analysis"] = analysis
        elif event["type"] in ["mouse_click", "key_press"]:
            if screenshot_path:
                analysis = self.ollama.vision_analysis([screenshot_path], f"Analyze this {event['type']} event.")
                event["visual_analysis"] = analysis

    def _capture_screenshot(self, event: Dict) -> Optional[str]:
        """Capture contextual screenshot with intelligent framing."""
        try:
            filename = f"{self.screenshot_dir}/{event['timestamp']}_{event['type']}.png"
            with ImageGrab.grab() as screenshot:
                screenshot.save(filename)
            return filename
        except Exception as e:
            logging.error(f"Screenshot capture failed: {str(e)}")
            return None

    # Event handlers with improved contextual recording
    def on_move(self, x: int, y: int):
        self.record_event("mouse_move", {"x": x, "y": y})

    def on_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        self.record_event(
            "mouse_click",
            {"x": x, "y": y, "button": button.name, "state": "pressed" if pressed else "released"}
        )

    def on_scroll(self, x: int, y: int, dx: int, dy: int):
        self.record_event("mouse_scroll", {"x": x, "y": y, "dx": dx, "dy": dy})

    def on_press(self, key: keyboard.Key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        self.record_event("key_press", {"key": char})

    def on_release(self, key: keyboard.Key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        self.record_event("key_release", {"key": char})

class EnhancedGUI(tk.Tk):
    """Modern GUI with improved user experience and real-time feedback."""
    def __init__(self):
        super().__init__()
        self.title("Autonomie Pro")
        self.geometry("800x600")
        self.recorder = EnhancedRecorder()
        self.ollama = OllamaManager()
        self._create_widgets()
        self._setup_keybindings()
        self.update_status("Ready")
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def _create_widgets(self):
        # Control Panel
        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X)
        self.record_btn = tk.Button(control_frame, text="⏺ Start Recording", command=self.toggle_recording)
        self.record_btn.pack(side=tk.LEFT, padx=5)
        self.playback_btn = tk.Button(control_frame, text="▶ Playback", command=self.playback)
        self.playback_btn.pack(side=tk.LEFT, padx=5)
        # Analysis Panel
        analysis_frame = tk.Frame(self)
        analysis_frame.pack(fill=tk.BOTH, expand=True)
        self.conversation_log = scrolledtext.ScrolledText(analysis_frame, state='disabled')
        self.conversation_log.pack(fill=tk.BOTH, expand=True)
        # Status Bar
        self.status_bar = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_keybindings(self):
        self.bind("<Control-r>", lambda e: self.toggle_recording())
        self.bind("<Control-p>", lambda e: self.playback())
        self.bind("<Control-q>", lambda e: self.quit())

    def toggle_recording(self):
        if not self.recorder.listeners or not any(l.is_alive() for l in self.recorder.listeners):
            self.recorder.start_recording()
            self.record_btn.config(text="⏹ Stop Recording", fg="red")
            self.update_status("Recording...")
        else:
            self.recorder.stop_recording()
            self.record_btn.config(text="⏺ Start Recording", fg="black")
            self.update_status("Recording stopped")

    def playback(self):
        """Reconstruct recorded actions using neural network analysis."""
        if not self.recorder.actions:
            messagebox.showwarning("Playback", "No recorded actions to play back.")
            return

        self.update_status("Analyzing recorded actions...")
        try:
            # Use the vision model to validate the current screen state
            screenshot_path = self._capture_current_screenshot()
            if not screenshot_path:
                raise RuntimeError("Failed to capture screenshot for playback validation.")

            # Analyze the current screen state
            analysis_prompt = (
                "Analyze this screenshot and determine if it matches the expected "
                "application state for playback."
            )
            analysis_result = self.ollama.vision_analysis([screenshot_path], analysis_prompt)
            logging.info(f"Playback validation result: {analysis_result}")

            # Check if the analysis indicates readiness for playback
            if "ready" not in analysis_result.lower():
                messagebox.showwarning(
                    "Playback",
                    "The current screen state does not match the expected state for playback."
                )
                self.update_status("Playback aborted due to mismatched screen state.")
                return

            # Proceed with playback
            self.update_status("Starting playback...")
            playback_thread = threading.Thread(target=self._execute_playback)
            playback_thread.start()

        except Exception as e:
            logging.error(f"Playback failed: {str(e)}")
            messagebox.showerror("Error", f"Playback failed: {str(e)}")
            self.update_status("Playback failed.")

    def _capture_current_screenshot(self) -> Optional[str]:
        """Capture the current screen state for validation."""
        try:
            filename = f"{self.recorder.screenshot_dir}/playback_validation_{time.time()}.png"
            with ImageGrab.grab() as screenshot:
                screenshot.save(filename)
            return filename
        except Exception as e:
            logging.error(f"Screenshot capture failed: {str(e)}")
            return None

    def _execute_playback(self):
        """Execute recorded actions with precise timing."""
        try:
            last_timestamp = None
            for action in self.recorder.actions:
                # Calculate delay between events
                if last_timestamp:
                    delay = action["timestamp"] - last_timestamp
                    time.sleep(max(0, delay))  # Ensure non-negative delay
                last_timestamp = action["timestamp"]

                # Reconstruct the action
                event_type = action["type"]
                details = action["details"]

                if event_type == "mouse_move":
                    self.mouse_controller.position = (details["x"], details["y"])
                elif event_type == "mouse_click":
                    button = mouse.Button.left if details["button"] == "left" else mouse.Button.right
                    if details["state"] == "pressed":
                        self.mouse_controller.press(button)
                    else:
                        self.mouse_controller.release(button)
                elif event_type == "mouse_scroll":
                    self.mouse_controller.scroll(details["dx"], details["dy"])
                elif event_type == "key_press":
                    key = self._map_key(details["key"])
                    self.keyboard_controller.press(key)
                elif event_type == "key_release":
                    key = self._map_key(details["key"])
                    self.keyboard_controller.release(key)

            self.update_status("Playback completed successfully.")
        except Exception as e:
            logging.error(f"Playback execution failed: {str(e)}")
            self.update_status("Playback failed during execution.")

    def _map_key(self, key_str: str) -> Union[keyboard.Key, str]:
        """Map string representation of keys to pynput Key objects."""
        special_keys = {
            "Key.enter": keyboard.Key.enter,
            "Key.space": keyboard.Key.space,
            "Key.backspace": keyboard.Key.backspace,
            "Key.tab": keyboard.Key.tab,
            "Key.shift": keyboard.Key.shift,
            "Key.ctrl": keyboard.Key.ctrl,
            "Key.alt": keyboard.Key.alt,
            "Key.cmd": keyboard.Key.cmd,
            "Key.esc": keyboard.Key.esc,
            "Key.up": keyboard.Key.up,
            "Key.down": keyboard.Key.down,
            "Key.left": keyboard.Key.left,
            "Key.right": keyboard.Key.right,
        }
        return special_keys.get(key_str, key_str)

    def update_status(self, message: str):
        self.status_bar.config(text=f"Status: {message}")
        self.update_idletasks()

    def log_conversation(self, message: str, is_user: bool = True):
        self.conversation_log.config(state='normal')
        prefix = "You: " if is_user else "AI: "
        self.conversation_log.insert(tk.END, prefix + message + "\n")
        self.conversation_log.config(state='disabled')
        self.conversation_log.see(tk.END)

    def start_chat(self):
        user_input = simpledialog.askstring("Chat", "Enter your message:")
        if user_input:
            self.log_conversation(user_input)
            response = self.ollama.chat_completion([{
                "role": "user",
                "content": user_input
            }])
            self.log_conversation(response, is_user=False)

def validate_environment():
    """Check for required dependencies and environment setup."""
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error("Ollama not installed or not in PATH")
        raise RuntimeError("Ollama not found. Please install and configure Ollama.")

if __name__ == "__main__":
    try:
        validate_environment()
        app = EnhancedGUI()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Application failed: {str(e)}", exc_info=True)
        messagebox.showerror("Critical Error", "Application encountered a critical error")
        sys.exit(1)
