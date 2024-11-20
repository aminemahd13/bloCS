house_blocks = {
    "Dirt": [],
    "Stone": [],
    "Wood": [
        # Adding a big rectangle made out of wood

    ],
    "Background": [],
    "Wood2": [],
    "Obsidian": [],
    "Bedrock": [],
    "Doorup": [],
    "Doordown": [],
    "Wood1": []
}


# Add rectangle coordinates
for x in range(20, 50):  # width of 5
    for y in range(8,25):  # height of 3
        house_blocks["Wood"].append((x, y))