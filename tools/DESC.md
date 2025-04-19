#### translate.py

This script is used to translate a file from one language to another using
Google Translate API. It takes a file path, source language, and target language
as input arguments. The script reads the content of the file, translates it,
and writes the translated content to a new file.

#### Usage

```bash
python translate.py source target from_lang to_lang
```

#

### yt_thumb.py

Scrape thumbnails from YouTube of all videos in the specified directory. The filename should have the IDs in square brackets
`filename [video_id].ext` for the script to work. The `yt_thumb.sh` does the same thing.

#### Usage

```bash
python yt_thumb.py path ## use -h for help
```

### yt_metadata.py

Scrape metadata from YouTube of all videos in the specified directory. The filename should have the IDs in square
`filename [video_id].ext` for the script to work.

#### Usage

```bash
python yt_metadata.py path ## use -h for help
```

### yt_toolkit.py

Merges functions from `yt_thumb.py` and `yt_metadata.py` into one script. It can scrape both thumbnails
and metadata from YouTube

#### Usage

```bash
python yt_toolkit.py path --thumb --nfo ## use -h for help
```