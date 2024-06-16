#!/bin/bash

# Check if the directory path is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

TARGET_DIR="$1"

# Check if the provided path is a valid directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR is not a valid directory."
    exit 1
fi

# Change to the target directory
cd "$TARGET_DIR" || exit

# Function to convert HEIC to JPG and delete the original HEIC files
convert_and_delete_heic() {
    find . -type f \( -iname "*.heic" -o -iname "*.HEIC" \) | while read -r file; do
        magick mogrify -format jpg "$file"
        rm "$file"
    done
}

# Function to remove EXIF data from JPG, JPEG, and PNG files
remove_exif_data() {
    exiftool -all= -ext jpg -ext jpeg -ext png .
}

# Run the functions
convert_and_delete_heic
remove_exif_data

echo "Conversion and EXIF removal complete."

