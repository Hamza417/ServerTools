import os
import re
import requests
import argparse

def download_thumbnail(video_id, save_path):
    """Download YouTube thumbnail and overwrite if exists."""
    url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(url)

    if response.status_code != 200:
        url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download thumbnail for ID: {video_id}")

def process_directory(directory):
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm')
    id_pattern = re.compile(r'\[([A-Za-z0-9_-]{11})\]$')  # Accepts hyphens and underscores

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            match = id_pattern.search(base)
            if match:
                video_id = match.group(1)
                output_filename = f"{base}-poster.jpg"
                save_path = os.path.join(directory, output_filename)

                download_thumbnail(video_id, save_path)
            else:
                print(f"No YouTube ID found in: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube thumbnails for video files with IDs in square brackets.'
    )
    parser.add_argument(
        'directory',
        type=str,
        help='Path to the directory containing video files.'
    )
    args = parser.parse_args()

    target_directory = os.path.abspath(os.path.expanduser(args.directory.replace('\\', '')))

    if os.path.isdir(target_directory):
        process_directory(target_directory)
    else:
        print(f"Error: '{target_directory}' is not a valid directory.")

if __name__ == "__main__":
    main()

