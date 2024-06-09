from pathlib import Path
import re
import sys
from typing import List, Set, Dict

def find_folders(path: Path, pattern: str) -> List[Path]: 
    return [f for f in path.iterdir() if f.is_dir() and re.match(pattern, f.name)]

def find_nonexistent_image_references(folder_images_path: Path, image_references: List[str]) -> List[str]:
    nonexistent_references = []
    for ref in image_references:
        if not (folder_images_path / ref).is_file():
            nonexistent_references.append(ref)
    return nonexistent_references

def get_markdown_image_references(md_file_path: Path) -> List[str]:
    with md_file_path.open('r') as file:
        content = file.read()
    # Markdown image syntax ![alt text](image_path)
    return re.findall(r'!\[.*?\]\((.*?)\)', content)

def check_images_used(folder_path: Path, image_references: List[str], ignore_list: Set[str]) -> Set[str]:
    images_in_folder = {f.name for f in folder_path.iterdir() if f.is_file() and f.name not in ignore_list}
    return images_in_folder - set(image_references)

def read_ignore_list(folder: Path) -> Set[str]:
    ignore_file = folder / "ignore_images"
    if ignore_file.is_file():
        with ignore_file.open('r') as file:
            return set([f.strip() for f in file.readlines()]) | {'ignore_images'}
    return {'ignore_images'}

def main() -> None:
    posts_path = Path("content", "en", "posts")
    images_path = Path("static", "images")

    folder_pattern = r'^\d{6}$'
    folders = find_folders(posts_path, folder_pattern)
    print(f"Found folders: {folders}")

    alert_message = []

    for folder in folders:
        md_file_path = folder / f"{folder.name}.md"
        if md_file_path.is_file():
            image_references = get_markdown_image_references(md_file_path)
            image_references = [Path(ref).name for ref in image_references]  # Extract image names
            print(f"Image references for {folder}: {image_references}")

            folder_images_path = images_path / folder.name
            if folder_images_path.is_dir():
                ignore_list = read_ignore_list(folder_images_path)
                print(f"Ignore list for {folder}: {ignore_list}")
                print(f"Images in {folder}: {folder_images_path}")
                unused_images = check_images_used(folder_images_path, image_references, ignore_list)
                nonexistent_references = find_nonexistent_image_references(folder_images_path, image_references)
                
                if unused_images:
                    alert_message.append(f"Unused images found in folder {folder}: {', '.join(unused_images)}")
                if nonexistent_references:
                    alert_message.append(f"References pointing to non-existent images in folder {folder}: {', '.join(nonexistent_references)}")

    if alert_message:
        print("Alerts:")
        for alert in alert_message:
            print(alert)
        sys.exit(1)
    else:
        print("No alerts.")
        sys.exit(0)

if __name__ == "__main__":
    main()

"""
```
# Image Checker

The Image Checker is a Python script designed to ensure consistency between images referenced in Markdown files and images present in corresponding folders. It alerts users to discrepancies such as unused images or missing references.

## Features

- Recursively searches for Markdown files and corresponding image folders.
- Compares images referenced in Markdown files with images present in folders.
- Detects unused images in folders and missing references in Markdown files.
- Supports custom ignore lists for images.

## Usage

1. **Installation:**
   - Clone the repository or download the script file.

2. **Setup:**
   - Place your Markdown files in a directory structured `/content/en/posts` where each month's posts are in the format MMDDDD (e.g., 062025).
   - Store your images in a similar directory structure under `/static/images`, where each post has its folder in the format MMDDDD (e.g., 062025).

3. **Configuration:**
   - Optionally, create an `ignore_images` file in each image folder to specify images to ignore.

4. **Running the Script:**
   - Execute the Python script `check_images.py`.
   - You can run it from the command line or integrate it into your workflow.

5. **Reviewing Alerts:**
   - The script will print alerts if it detects discrepancies between images and references.
   - Review the alerts to identify and resolve any issues.

## Example

Consider the following folder structure:

```
/content
    /en
        /posts
            /202201
                202201.md
/static
    /images
        /202201
            image1.jpg
            image2.jpg
```

- If `202201.md` references `image1.jpg` but not `image2.jpg`, the script will raise an alert for the missing reference.
- If `image2.jpg` is present but not referenced in `202201.md`, the script will raise an alert for the unused image.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
"""