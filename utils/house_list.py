house_blocks = {
    "Dirt": [],
    "Stone": [],
    "Wood": [],
    "Doordown": [[38,7], [39,7]],      # Top part of doors
    "Doorup": [[38,6], [39,6]],     # Bottom part of doors
    "Background": [],
    "Wood2": [],
    "Obsidian": [],
    "Bedrock": [],
    "Wood1": [],
    "Game" : [[36 , 7]]
}


# Add rectangle coordinates
for x in range(20, 50):  # width of 5
    for y in range(8,25):  # height of 3
        house_blocks["Wood"].append((x, y))