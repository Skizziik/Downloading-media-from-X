# X/Twitter Media Downloader

A script for downloading media (videos and images) from X (Twitter) platform in maximum quality.

## Features

- Download videos and images from X/Twitter
- Batch download support (multiple links at once)
- Automatic maximum quality detection
- Simple text file for link management
- Custom download directory selection

## Requirements

- Python 3.6+
- requests library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Skizziik/Downloading-media-from-X.git
cd Downloading-media-from-X
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Open `links.txt` file and add X/Twitter post links (one link per line):
```
https://x.com/username/status/1234567890
https://twitter.com/username/status/0987654321
```

2. Run the script:
```bash
python download_media.py
```

3. Specify download folder (or press Enter for default folder)

4. The script will automatically:
   - Extract all media from specified posts
   - Download them in maximum available quality
   - Save to the specified folder

## File Structure

- `download_media.py` - main script
- `links.txt` - file with post links (one link per line)
- `requirements.txt` - Python dependencies
- `downloads/` - default folder for saving media

## Supported Link Formats

The following link formats are supported:
- `https://x.com/username/status/1234567890`
- `https://twitter.com/username/status/1234567890`

## Features

- Automatic media type detection (video/image)
- Progress bar for download tracking
- Error handling and retry attempts
- Unique filenames with timestamps

## Notes

- The script uses public APIs to fetch media
- Please respect copyright when downloading content
- Some private accounts may not be accessible

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Issues

If you encounter any problems, please create an [issue](https://github.com/Skizziik/Downloading-media-from-X/issues)