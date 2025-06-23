import yt_dlp
import os
import re # For extracting filename from metadata

def download_youtube_video(url, quality, output_template):
    # yt-dlp options based on requested quality
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if quality == 'best' else quality,
        'outtmpl': output_template,
        'noplaylist': True, # Only download single video
        'progress_hooks': [], # Can add hooks for progress bar if needed
        'quiet': True, # Suppress console output for cleaner Flask integration
        'no_warnings': True,
    }

    downloaded_file_path = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False) # Get info without downloading
            video_title = info_dict.get('title', 'video')
            # Sanitize title for filename
            safe_title = re.sub(r'[\\/:*?"<>|]', '', video_title)

            # Update output template to include sanitized title and original extension
            final_output_template = os.path.join(
                os.path.dirname(output_template), 
                f"{safe_title}_{os.path.basename(output_template).split('.')[0]}.%(ext)s"
            )
            ydl_opts['outtmpl'] = final_output_template

            # Now download with the updated template
            download_result = ydl.download([url])

            # yt-dlp stores the downloaded file path in info_dict after download
            # Or you can construct it based on the outtmpl and extracted info
            downloaded_files = ydl.download_result['files']
            if downloaded_files:
                # If multiple files are downloaded (e.g., separate video/audio),
                # you might need more complex logic. For 'best', it's usually one merged file.
                downloaded_file_path = downloaded_files[0]

            if downloaded_file_path is None or not os.path.exists(downloaded_file_path):
                 raise Exception("yt-dlp did not report a downloaded file path or file not found.")

    except yt_dlp.utils.DownloadError as e:
        raise ValueError(f"YouTube download error: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred during download: {e}")

    return downloaded_file_path