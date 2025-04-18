#!/bin/bash

show_help() {
    echo "Usage: $0 [options] /path/to/directory"
    echo ""
    echo "Options:"
    echo "  -q, --quiet         Suppress output (silent mode)"
    echo "  -m, --missing-only  Only download thumbnails if -poster.jpg does not exist"
    echo "  -h, --help          Show this help message"
}

# Default flags
QUIET=false
MISSING_ONLY=false

# Parse arguments
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -m|--missing-only)
            MISSING_ONLY=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

# Check directory argument
if [ ${#POSITIONAL[@]} -ne 1 ]; then
    show_help
    exit 1
fi

DIRECTORY="${POSITIONAL[0]}"

if [ ! -d "$DIRECTORY" ]; then
    echo "Error: '$DIRECTORY' is not a valid directory."
    exit 1
fi

# Display mode info
if $QUIET; then
    echo "Running in quiet mode: No output will be shown unless an error occurs."
fi
if $MISSING_ONLY; then
    echo "Running in 'missing-only' mode: Only missing thumbnails will be downloaded."
fi

EXTENSIONS=("mp4" "mkv" "avi" "mov" "flv" "webm")

for file in "$DIRECTORY"/*; do
    filename=$(basename "$file")
    extension="${filename##*.}"
    base="${filename%.*}"

    for ext in "${EXTENSIONS[@]}"; do
        if [[ "${extension,,}" == "$ext" ]]; then
            # Extract YouTube ID from square brackets
            if [[ "$base" =~ \[([A-Za-z0-9_-]{11})\]$ ]]; then
                video_id="${BASH_REMATCH[1]}"
                output_path="$DIRECTORY/$base-poster.jpg"

                # Skip if missing-only is active and thumbnail exists
                if $MISSING_ONLY && [ -f "$output_path" ]; then
                    $QUIET || echo "Skipping: Thumbnail already exists for '$filename'."
                    break
                fi

                # Notify about the thumbnail download process
                $QUIET || echo "Downloading thumbnail for '$filename'..."

                # Try maxresdefault first
                url="https://img.youtube.com/vi/$video_id/maxresdefault.jpg"
                if curl --silent --head --fail "$url" > /dev/null; then
                    curl -s "$url" -o "$output_path"
                    $QUIET || echo "Downloaded: $output_path"
                else
                    url="https://img.youtube.com/vi/$video_id/hqdefault.jpg"
                    if curl --silent --head --fail "$url" > /dev/null; then
                        curl -s "$url" -o "$output_path"
                        $QUIET || echo "Downloaded (fallback): $output_path"
                    else
                        $QUIET || echo "Failed to download thumbnail for ID: $video_id"
                    fi
                fi
            else
                $QUIET || echo "No YouTube ID found in: $filename"
            fi
            break
        fi
    done
done
