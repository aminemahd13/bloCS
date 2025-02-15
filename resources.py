import os
import sys

def resources(relative_path):
    """Get the absolute path to the resource."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Example usage
image_path = resources("assets/graphics/example.png")
audio_path = resources("assets/audio/example.mp3")
