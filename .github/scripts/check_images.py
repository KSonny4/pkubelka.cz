from pathlib import Path
import re
import sys
from typing import List, Set, Dict

def find_folders(path: Path, pattern: str) -> List[Path]: 
    return [f for f in path.iterdir() if f.is_dir() and re.match(pattern, f.name)]

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
    posts_path = Path("/content", "en", "posts")
    images_path = Path("/static", "images")
    
    folder_pattern = r'^\d{6}$'
    folders = find_folders(posts_path, folder_pattern)
    print(f"Found folders: {folders}")

    all_unused_images: Dict[str, Set[str]] = {}

    for folder in folders:
        md_file_path = folder / f"{folder.name}.md"
        if md_file_path.is_file():
            image_references = get_markdown_image_references(md_file_path)
            image_references = [Path(ref).name for ref in image_references]  # Extract image names
            print(f"Images for {folder}: {image_references}")

            folder_images_path = images_path / folder.name
            if folder_images_path.is_dir():
                ignore_list = read_ignore_list(folder_images_path)
                print(f"Ignore list: {ignore_list}")
                unused_images = check_images_used(folder_images_path, image_references, ignore_list)
                if unused_images:
                    all_unused_images[folder.name] = unused_images

    if all_unused_images:
        print("Unused images found:")
        for folder, images in all_unused_images.items():
            print(f"Folder: {folder}")
            for image in images:
                print(f" - {image}")
        sys.exit(1)
    else:
        print("No unused images found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
