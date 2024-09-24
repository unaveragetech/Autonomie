import cv2
import pytesseract
import pyautogui
import numpy as np
import uuid
import json
from engine.memory_manager import MemoryManager

class ObjectRecognitionEngine:
    def __init__(self, cli):
        self.cli = cli
        self.memory_manager = MemoryManager()
        self.cli.log("Object Recognition Engine initialized")

    def capture_screen(self):
        """Capture a screenshot of the screen."""
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        return cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

    def recognize_text(self, image):
        """Recognize text from the image using Tesseract OCR."""
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image)
        return text.strip()

    def detect_objects(self, image):
        """Detect objects (icons, buttons) using shape recognition with OpenCV."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        objects = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            x, y, w, h = cv2.boundingRect(approx)
            
            if w > 50 and h > 50:  # Ignore very small objects
                object_id = str(uuid.uuid4())
                roi = image[y:y+h, x:x+w]
                recognized_text = self.recognize_text(roi)
                tag = "button" if "submit" in recognized_text.lower() else "label" if recognized_text else "icon"
                color = self.detect_color(image, x, y)

                object_data = {
                    "id": object_id,
                    "tag": tag,
                    "coordinates": {"x": x, "y": y, "width": w, "height": h},
                    "properties": {"shape": "rectangle", "color": color, "text": recognized_text}
                }

                objects.append(object_data)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return objects

    def detect_color(self, image, x, y):
        """Detect the color of the object at the given coordinates (x, y)."""
        b, g, r = image[y, x]
        return (r, g, b)

    def process_screen(self):
        """Main function to capture the screen, recognize objects, and update memory."""
        screen_image = self.capture_screen()
        recognized_objects = self.detect_objects(screen_image)
        
        for obj in recognized_objects:
            existing_obj = self.memory_manager.find_matching_object(obj)
            if existing_obj:
                obj['id'] = existing_obj['id']
                self.cli.log(f"Recurring object detected: {obj['id']} (Tag: {obj['tag']})")
            else:
                self.memory_manager.add_object(obj)
                self.cli.log(f"New object detected: {obj['id']} (Tag: {obj['tag']})")

        self.memory_manager.save_memory()
        cv2.imshow('Screen with Detected Objects', screen_image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
