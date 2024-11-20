from PIL import Image

#Aller sur pixilart.com
#Choisir une taille de 39 px * 27 px
#Aller dans le choix des palettes de couleur
#Choisir "EGA Graphics (RGB)" by PixelPen

#Obsidienne : violet
#Terre : rouge
#Bloc "d'air" : jaune
#Bedrock : noir
#Pierre : vert

longueur_image = 39
hauteur_image = 27
x_min = -2
x_max = 3
y_min = 0
y_max = 2

# Create a dictionary to store coordinates for each color
color_coordinates = {}

for x_map in range(x_min , x_max + 1):
    for y_map in range(y_min , y_max + 1):
        # Load the image
        image_path = "./crea_map/images/images2/"+ str(x_map) + "_" + str(y_map) + ".png"
        print(image_path)
        image = Image.open(image_path)

        # Get image size and convert to RGB
        pixels = image.convert("RGB")
        width, height = image.size

        # Loop through each pixel to extract color and coordinates
        for y in range(height):
            for x in range(width):
                color = pixels.getpixel((x, y))
                if color not in color_coordinates:
                    color_coordinates[color] = []
                color_coordinates[color].append([x_map * 39 + x , y_map * 27 + y])


# Display results
for key , values in color_coordinates.items():
    for i in range(5):
        print(" ")
    print(key)
    print(values)