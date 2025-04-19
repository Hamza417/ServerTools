import os
import re
import requests
import argparse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv


def fetch_youtube_metadata(video_id, api_key):
    """Fetch metadata from YouTube Data API."""
    url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=snippet&id={video_id}&key={api_key}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get('items')
        if items:
            snippet = items[0]['snippet']
            return {
                'title': snippet['title'],
                'description': snippet['description'],
                'upload_date': snippet['publishedAt'][:10],
                'channel_title': snippet['channelTitle'],
                'tags': snippet.get('tags', [])
            }
    return None


def write_nfo(metadata, save_path):
    """Write metadata to an NFO file in XML format."""
    root = ET.Element("movie")
    ET.SubElement(root, "title").text = metadata['title']
    ET.SubElement(root, "plot").text = metadata['description']
    ET.SubElement(root, "premiered").text = metadata['upload_date']
    ET.SubElement(root, "studio").text = metadata['channel_title']

    for tag in metadata['tags']:
        ET.SubElement(root, "tag").text = tag

    tree = ET.ElementTree(root)
    tree.write(save_path, encoding="utf-8", xml_declaration=True)


def process_directory(directory, api_key, quiet=False, missing_only=False):
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm')
    id_pattern = re.compile(r'\[([A-Za-z0-9_-]{11})\]$')

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            match = id_pattern.search(base)
            if match:
                video_id = match.group(1)
                output_filename = f"{base}.nfo"
                save_path = os.path.join(directory, output_filename)

                if missing_only and os.path.exists(save_path):
                    if not quiet:
                        print(f"Skipping: NFO already exists for '{filename}'.")
                    continue

                if not quiet:
                    print(f"Fetching metadata for '{filename}'...")
                metadata = fetch_youtube_metadata(video_id, api_key)

                if metadata:
                    write_nfo(metadata, save_path)
                    if not quiet:
                        print(f"Saved NFO: {output_filename}")
                else:
                    print(f"Failed to fetch metadata for ID: {video_id}")
            else:
                if not quiet:
                    print(f"No YouTube ID found in: {filename}")


def main():
    load_dotenv()  # Load .env file
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment.")
        return

    parser = argparse.ArgumentParser(
        description='Download YouTube metadata and create NFO files for video files with IDs in square brackets.'
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
        help='Only create NFO files if they do not exist.'
    )

    args = parser.parse_args()
    target_directory = os.path.abspath(os.path.expanduser(args.directory.replace('\\', '')))

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        return

    if args.quiet:
        print("Running in quiet mode: Only errors will be shown.")
    if args.missing_only and not args.quiet:
        print("Running in 'missing-only' mode: Skipping files with existing NFOs.")

    process_directory(
        target_directory,
        api_key,
        quiet=args.quiet,
        missing_only=args.missing_only
    )


if __name__ == "__main__":
    main()
