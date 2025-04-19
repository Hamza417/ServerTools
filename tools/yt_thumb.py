import os
import re
import requests
import argparse

def download_thumbnail(video_id, save_path, quiet):
    """Download YouTube thumbnail, overwrite if exists."""
    url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(url)

    if response.status_code != 200:
        url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        if not quiet:
            print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download thumbnail for ID: {video_id}")

def process_directory(directory, quiet=False, missing_only=False):
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm')
    id_pattern = re.compile(r'\[([A-Za-z0-9_-]{11})\]$')

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            match = id_pattern.search(base)
            if match:
                video_id = match.group(1)
                output_filename = f"{base}-poster.jpg"
                save_path = os.path.join(directory, output_filename)

                if missing_only and os.path.exists(save_path):
                    if not quiet:
                        print(f"Skipping: Thumbnail already exists for '{filename}'.")
                    continue

                if not quiet:
                    print(f"Downloading thumbnail for '{filename}'...")
                download_thumbnail(video_id, save_path, quiet)
            else:
                if not quiet:
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
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress non-error output.'
    )
    parser.add_argument(
        '-m', '--missing-only',
        action='store_true',
        help='Only download thumbnails if the poster file does not exist.'
    )

    args = parser.parse_args()

    target_directory = os.path.abspath(os.path.expanduser(args.directory.replace('\\', '')))

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        return

    # Startup mode info
    if args.quiet:
        print("Running in quiet mode: Only errors will be shown.")
    if args.missing_only:
        if not args.quiet:
            print("Running in 'missing-only' mode: Skipping files with existing thumbnails.")

    process_directory(target_directory, quiet=args.quiet, missing_only=args.missing_only)

if __name__ == "__main__":
    main()
