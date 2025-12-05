import os
import yt_dlp

# ==========================
#  Load & Save Downloaded Video IDs
# ==========================

downloaded_ids_file = "downloaded_ids.txt"

if os.path.exists(downloaded_ids_file):
    with open(downloaded_ids_file, "r") as f:
        downloaded_ids = set(line.strip() for line in f)
else:
    downloaded_ids = set()

def save_video_id(video_id):
    with open(downloaded_ids_file, "a") as f:
        f.write(video_id + "\n")

# ==========================
#  Custom Progress Bar
# ==========================

def progress_hook(d):
    info = d.get('info_dict', {})
    title = info.get('title', 'Loading...')
    video_id = info.get('id')

    index = info.get('playlist_index')
    if index is None:
        index = 1

    # If skipped
    if video_id in downloaded_ids:
        print(f"\r⏭️ [{index:02d}] {title} – SKIPPED (Already Downloaded)", end='')
        return

    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').replace(" ", "")
        speed = d.get('_speed_str', '0 KB/s')
        eta = d.get('_eta_str', '?')
        print(f"\r🎵 [{index:02d}] {title} – {percent} | {speed} | ETA: {eta}", end='')

    elif d['status'] == 'finished':
        print(f"\r🎵 [{index:02d}] {title} – 100% | Completed")
        print("🔄 Converting to MP3...")
        save_video_id(video_id)

# ==========================
#  Playlist link
# ==========================

playlist_url = input("Enter YouTube Playlist Link: ")

output_folder = r"C:\Users\Abhijith.AK\Desktop\Abhijith\Me\youtube\songs"
os.makedirs(output_folder, exist_ok=True)

FFMPEG_LOCATION = r"C:\ffmpeg-2025-12-01-git-7043522fe0-full_build\bin\ffmpeg.exe"

# ==========================
#  match_filter FIXED
# ==========================

def skip_if_duplicate(info_dict, *args, **kwargs):
    video_id = info_dict.get("id")
    if video_id in downloaded_ids:
        return "already downloaded"   # skip reason → yt-dlp will skip
    return None  # OK to download

# ==========================
#  Options
# ==========================

ydl_opts = {
    'format': 'bestaudio/best',

    'extractor_args': {'youtube': {'player_client': ['default']}},

    'outtmpl': os.path.join(output_folder, '%(playlist_index|1)02d - %(title)s.%(ext)s'),

    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

    'ffmpeg_location': FFMPEG_LOCATION,

    'match_filter': skip_if_duplicate,   # <-- FIXED

    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [progress_hook],
}

# ==========================
#  Start download
# ==========================

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])

print("\n\n✅ All MP3 files saved in:", output_folder)
print("🛡 Duplicate protection active (video ID check)")
