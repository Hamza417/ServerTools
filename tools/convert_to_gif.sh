#!/bin/bash

# Optional: set Internal Field Separator to handle filenames with spaces/newlines
IFS=$'\n'

for f in *.mp4; do
    [ -f "$f" ] || continue

    base="${f%.mp4}"
    palette="${base}-palette.png"
    gif="${base}.gif"

    echo "🎞️ Processing \"$f\"..."

    # Step 1: Generate color palette
    ffmpeg -y -i "$f" \
        -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" \
        -frames:v 1 "$palette"

    # Step 2: Create GIF using palette
    ffmpeg -y -i "$f" -i "$palette" \
        -filter_complex "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" \
        "$gif"

    # Cleanup
    rm -f "$palette"
    rm -f "$f"

    echo "✅ Converted \"$f\" → \"$gif\" and deleted original."
done
