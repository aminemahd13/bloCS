import keyboard



print("Press 'Esc' to exit.")

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:  # Only process key-down events
        print(f"Key '{event.name}' pressed")
    if event.name == 'esc':
        print("Exiting...")
        break
