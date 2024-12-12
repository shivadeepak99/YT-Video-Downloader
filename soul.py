from yt_dlp import YoutubeDL
import os
import sys
import json
from re import sub

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')

if len(sys.argv) < 2:
    print(json.dumps({"error": "Usage: python soul.py <url>"}))
    sys.exit(1)

url = sys.argv[1]

if not os.path.exists(ffmpeg_path):
    print(json.dumps({"error": "FFmpeg not found!"}))
    sys.exit(1)

def remove_non_encodable_chars(title, codec='charmap'):
    encodable_chars = []
    for char in title:
        try:
            char.encode(codec)
            encodable_chars.append(char)
        except UnicodeEncodeError:
            continue
    return ''.join(encodable_chars)

def progress_hook(d):
    if d['status'] == 'downloading':
        progress = {
            "progress": d['_percent_str'].strip(),
            "downloaded_bytes": d.get('downloaded_bytes', 0),
            "total_bytes": d.get('total_bytes', 0),
            "speed": d.get('_speed_str', 'N/A'),
            "eta": d.get('_eta_str', 'N/A'),
        }
        print(json.dumps(progress), flush=True)
    elif d['status'] == 'finished':
        print(json.dumps({"status": "finished", "file": d['filename']}), flush=True)

try:
    with YoutubeDL({'ffmpeg_location': ffmpeg_path}) as dp:
        info = dp.extract_info(url, download=False)
        title = remove_non_encodable_chars(info['title'])
        duration = info['duration']

        print(json.dumps({"title": title, "duration": duration}), flush=True)

        sanitized_title = sub(r'[\\/*?:"<>|]', "_", title)
        if len(sanitized_title) > 20:
            sanitized_title = sanitized_title[:20]

        download_folder = os.path.expanduser("~/Downloads")
        options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_folder, f"{sanitized_title}.mp4"),
            'ffmpeg_location': ffmpeg_path,
            'progress_hooks': [progress_hook],
        }

        with YoutubeDL(options) as dp:
            dp.download([url])
except Exception as e:
    print(json.dumps({"error": str(e)}), flush=True)
