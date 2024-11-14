import keyboard


class KeyHandler:
    def __init__(self):
        self.key = None
        self.directions = []  # List to store the directions
        self.direction_map = {
            "w": "haut",  # W key
            "up": "haut",  # Up arrow
            "s": "bas",  # S key
            "down": "bas",  # Down arrow
            "a": "gauche",  # A key
            "left": "gauche",  # Left arrow
            "d": "droite",  # D key
            "right": "droite",  # Right arrow
        }

    def get_pressed_key(self):
        """Capture the key press event and store the pressed key."""
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:  # Only process key-down events
            self.key = event.name
        return self.key

    def get_direction(self):
        """Capture a key press event and return the direction associated with it."""
        # Capture the key press event
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:  # Only process key-down events
            key = event.name
            return self.direction_map.get(
                key, None
            )  # Return the direction or None if the key isn't mapped
        return None


# Usage
#handler = KeyHandler()

# To listen for a direction, call the get_direction method
#direction = handler.get_direction()

# You can access the direction directly
#print(f"Direction: {direction}")
