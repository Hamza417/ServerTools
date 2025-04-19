import os
import re
import requests
import argparse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv


def download_thumbnail(video_id, save_path, silent_level):
    """Download YouTube thumbnail, overwrite if exists."""
    url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    response = requests.get(url)

    if response.status_code != 200:
        url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        if should_print('fetch', silent_level):
            print(f"Downloaded thumbnail: {save_path}")
    else:
        print(f"Failed to download thumbnail for ID: {video_id}")


def fetch_youtube_metadata(video_id, api_key):
    """Fetch metadata from YouTube Data API."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
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


def should_print(message_type, silent_level):
    """
    Controls print output based on silent level.
    message_type: 'skip', 'fetch', or 'error'
    """
    if silent_level == 2 and message_type != 'error':
        return False
    if silent_level == 1 and message_type == 'skip':
        return False
    return True


def process_directory(directory, api_key, silent_level=0, missing_only=False, do_thumbs=False, do_nfo=False):
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm')
    id_pattern = re.compile(r'\[([A-Za-z0-9_-]{11})\]$')

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() in video_extensions:
            match = id_pattern.search(base)
            if match:
                video_id = match.group(1)

                if do_thumbs:
                    thumb_filename = f"{base}-poster.jpg"
                    thumb_path = os.path.join(directory, thumb_filename)

                    if missing_only and os.path.exists(thumb_path):
                        if should_print('skip', silent_level):
                            print(f"Skipping: Thumbnail exists for '{filename}'.")
                    else:
                        if should_print('fetch', silent_level):
                            print(f"Downloading thumbnail for '{filename}'...")
                        download_thumbnail(video_id, thumb_path, silent_level)

                if do_nfo:
                    nfo_filename = f"{base}.nfo"
                    nfo_path = os.path.join(directory, nfo_filename)

                    if missing_only and os.path.exists(nfo_path):
                        if should_print('skip', silent_level):
                            print(f"Skipping: NFO exists for '{filename}'.")
                    else:
                        if should_print('fetch', silent_level):
                            print(f"Fetching metadata for '{filename}'...")
                        metadata = fetch_youtube_metadata(video_id, api_key)
                        if metadata:
                            write_nfo(metadata, nfo_path)
                            if should_print('fetch', silent_level):
                                print(f"Saved NFO: {nfo_filename}")
                        else:
                            print(f"Failed to fetch metadata for ID: {video_id}")
            else:
                if should_print('error', silent_level):
                    print(f"No YouTube ID found in: {filename}")


def main():
    load_dotenv()  # Load API Key from .env
    api_key = os.getenv('YOUTUBE_API_KEY')

    parser = argparse.ArgumentParser(
        description='YouTube Toolkit: Download thumbnails and create NFO metadata files.'
    )
    parser.add_argument(
        'directory',
        type=str,
        help='Path to the directory containing video files.'
    )
    parser.add_argument(
        '--thumbs',
        action='store_true',
        help='Download YouTube thumbnails.'
    )
    parser.add_argument(
        '--nfo',
        action='store_true',
        help='Download YouTube metadata and create NFO files.'
    )
    parser.add_argument(
        '-m', '--missing-only',
        action='store_true',
        help='Only process files missing thumbnails or NFOs.'
    )
    parser.add_argument(
        '--silent-level',
        type=int,
        choices=[0, 1, 2],
        default=0,
        help='Silence level: 0=Verbose, 1=Hide skipping lines, 2=Errors only.'
    )

    args = parser.parse_args()
    target_directory = os.path.abspath(os.path.expanduser(args.directory.replace('\\', '')))

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        return

    if not args.thumbs and not args.nfo:
        print("Error: No operation specified. Use --thumbs and/or --nfo.")
        return

    if args.nfo and not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment, required for NFO.")
        return

    if args.silent_level == 2:
        print("Running in full quiet mode: Only errors will be shown.")
    elif args.silent_level == 1:
        print("Running in pseudo-quiet mode: Skipping lines will be hidden.")
    elif args.missing_only:
        print("Running in 'missing-only' mode: Skipping files with existing outputs.")

    process_directory(
        target_directory,
        api_key,
        silent_level=args.silent_level,
        missing_only=args.missing_only,
        do_thumbs=args.thumbs,
        do_nfo=args.nfo
    )


if __name__ == "__main__":
    main()
