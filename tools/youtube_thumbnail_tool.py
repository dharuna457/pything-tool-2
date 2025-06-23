import requests
import re
import os

def get_youtube_video_id(url):
    # Regex to extract video ID from various YouTube URL formats
    video_id_match = re.search(
        r'(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|)([a-zA-Z0-9_-]{11})(?:\S+)?',
        url
    )
    if video_id_match:
        return video_id_match.group(1)
    return None

def download_youtube_thumbnail(video_url, output_path):
    video_id = get_youtube_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL provided.")

    # Try highest quality (maxresdefault) first
    thumbnail_urls = [
        f"http://img.youtube.com/vi/{video_id}/maxresdefault.jpg", # Best quality
        f"http://img.youtube.com/vi/{video_id}/hqdefault.jpg",     # High quality
        f"http://img.youtube.com/vi/{video_id}/mqdefault.jpg",     # Medium quality
        f"http://img.youtube.com/vi/{video_id}/default.jpg"       # Standard quality
    ]

    downloaded = False
    for url in thumbnail_urls:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            # Check if the content-type is an image and if it's not a tiny error image
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type and int(response.headers.get('Content-Length', 0)) > 1000: # Minimal size check
                with open(output_path, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)
                downloaded = True
                break # Successfully downloaded
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Attempt to download from {url} failed: {e}")
            continue # Try next URL

    if not downloaded:
        raise ValueError("Could not find a valid thumbnail for the given YouTube video at any quality.")