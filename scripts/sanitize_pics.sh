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

# Function to convert HEIC to JPG and delete the original HEIC files
convert_and_delete_heic() {
    find "$TARGET_DIR" -type f \( -iname "*.heic" -o -iname "*.HEIC" \) | while read -r file; do
        magick mogrify -format jpg "$file"
    done
}

# Function to remove EXIF data from JPG, JPEG, and PNG files
remove_exif_data() {
    exiftool -r -all= -ext jpg -ext jpeg -ext png "$TARGET_DIR"
}

remove_originals() {
    fd  "$TARGET_DIR" '_original' -x rm
}

# Run the functions
convert_and_delete_heic
remove_exif_data
remove_originals

echo "Conversion and EXIF removal complete."
