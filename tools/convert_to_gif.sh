#!/bin/bash

for f in *.mp4; do
    [ -f "$f" ] || continue  # skip if no .mp4 files
    base="${f%.mp4}"
    palette="$base-palette.png"
    gif="$base.gif"

    echo "Processing $f..."

    ffmpeg -y -i "$f" -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" "$palette"
    ffmpeg -y -i "$f" -i "$palette" -vf "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" "$gif"
    
    rm "$palette"
    rm "$f"

    echo "Converted $f -> $gif and removed original."
done
