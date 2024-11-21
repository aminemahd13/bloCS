#!/bin/bash

# Define input and output directories
input_dir="./images"
output_dir="./resized"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate through all image files in the input directory
for image in "$input_dir"/*.{png,jpg,jpeg,gif}; do
    # Check if the file exists (handles cases with no matches)
    if [[ -e $image ]]; then
        # Get the base name of the image
        filename=$(basename "$image")
        # Resize the image and save it to the output directory
        convert "$image" -resize 20x20 "$output_dir/$filename"
        echo "Resized $filename to 20x20 pixels."
    fi
done

echo "All images have been resized and saved to the '$output_dir' directory."
