import json

class MemoryManager:
    def __init__(self):
        self.memory = {"elements": []}
        self.load_memory()

    def load_memory(self):
        """Load the memory of recognized elements from a JSON file."""
        try:
            with open('object_memory.json', 'r') as file:
                self.memory = json.load(file)
        except FileNotFoundError:
            self.memory = {"elements": []}
            print("No existing memory found, starting fresh.")

    def save_memory(self):
        """Save the recognized elements to a JSON file."""
        with open('object_memory.json', 'w') as file:
            json.dump(self.memory, file, indent=4)

    def add_object(self, obj):
        """Add a new object to memory."""
        self.memory['elements'].append(obj)

    def find_matching_object(self, new_object):
        """Find if an object is recurring by comparing it with memory."""
        for obj in self.memory['elements']:
            if self.is_similar(obj, new_object):
                return obj
        return None

    def is_similar(self, obj1, obj2):
        """Check if two objects are similar."""
        return obj1['properties']['size'] == obj2['properties']['size'] and \
               abs(obj1['coordinates']['x'] - obj2['coordinates']['x']) < 10 and \
               abs(obj1['coordinates']['y'] - obj2['coordinates']['y']) < 10
