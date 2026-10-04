import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

def isffmpegok():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def ffmpegohmygod():
    print("FFmpeg not found.")
    system = platform.system()
    try:
        if system == "Windows":
            print()
            print("Install FFmpeg with:")
            print("winget install Gyan.FFmpeg")
            input("Press Enter after installing...")
        elif system == "Darwin":
            subprocess.check_call(["brew", "install", "ffmpeg"])
        elif system == "Linux":
            if os.path.exists("/etc/arch-release"):
                subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"])
            elif os.path.exists("/etc/debian_version"):
                subprocess.check_call(["sudo", "apt", "update"])
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif os.path.exists("/etc/fedora-release"):
                subprocess.check_call(["sudo", "dnf", "install", "-y", "ffmpeg"])
            else:
                print("Install ffmpeg using your package manager.")
                input("Press Enter after installing...")
        return isffmpegok()
    except Exception as e:
        print(f"FFmpeg installation failed: {e}")
        return False

if not isffmpegok():
    if not ffmpegohmygod():
        print("FFmpeg is required.")
        sys.exit(1)

try:
    import yt_dlp
except ImportError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-U", "yt-dlp"
    ])
    import yt_dlp

def updatethisstupidthing():
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-U", "yt-dlp"
        ])
        print()
        print("yt-dlp updated successfully.")
    except Exception as e:
        print()
        print(f"Could not update yt-dlp: {e}")

def cleartheshit():
    os.system("cls" if os.name == "nt" else "clear")

def makeitlookcool(text, duration=0.5):
    chars = " .:-=+*#%@"
    steps = len(chars)
    sleep_time = duration / (steps * 2)

    for i in range(steps):
        faded = chars[i] * len(text)
        print(f"\r{faded}", end="", flush=True)
        time.sleep(sleep_time)

    for i in range(steps):
        idx = steps - 1 - i
        faded = chars[idx] * len(text)
        print(f"\r{faded}", end="", flush=True)
        time.sleep(sleep_time)

    print(f"\r{text}", flush=True)
    time.sleep(0.3)

def whereismydocuments():
    if os.name == "nt":
        return Path(os.environ.get("USERPROFILE", "")) / "Documents"
    return Path.home() / "Documents"

def putitthere(folder_name):
    print()
    print("Download folder")
    print("Enter a path or press Enter for the default folder")
    print()
    custom_path = input("Path: ").strip()

    if custom_path:
        output_dir = Path(custom_path).expanduser().resolve()
    else:
        output_dir = whereismydocuments() / folder_name

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def cookiesidk():
    print()
    print("Cookie source")
    print()
    print("  [1] None")
    print("  [2] Brave")
    print("  [3] Chrome")
    print("  [4] Firefox")
    print("  [5] Edge")
    print()

    choice = input("Choice: ").strip()

    browsers = {
        "2": "brave",
        "3": "chrome",
        "4": "firefox",
        "5": "edge"
    }

    if choice in browsers:
        return {
            "cookiesfrombrowser": (browsers[choice], None, None, None)
        }

    return {}

def fixthatyturl(url):
    try:
        parts = urlsplit(url)

        if "music.youtube.com" not in parts.netloc.lower():
            return url

        query = parse_qsl(parts.query, keep_blank_values=True)
        video_id = next((value for key, value in query if key == "v"), None)

        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

        return urlunsplit((
            "https",
            "www.youtube.com",
            parts.path,
            urlencode(query),
            ""
        ))
    except Exception:
        return url

def namingthing(is_playlist):
    if is_playlist:
        return "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"
    return "%(title)s.%(ext)s"

def maketheoptions(output_dir, is_playlist, cookies_opt):
    options = {
        "outtmpl": str(output_dir / namingthing(is_playlist)),
        "quiet": False,
        "no_warnings": False,
        "noplaylist": not is_playlist,
        "windowsfilenames": True,
        "retries": 3,
        "fragment_retries": 3,
        "ignoreerrors": True
    }

    if cookies_opt:
        options.update(cookies_opt)

    return options

def downloadthesong(url, output_dir, codec, is_playlist=False, cookies_opt=None):
    url = fixthatyturl(url)

    options = maketheoptions(
        output_dir,
        is_playlist,
        cookies_opt
    )

    options["format"] = "bestaudio/best"
    options["postprocessors"] = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": codec,
        "preferredquality": "320"
    }]

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def downloadthatvideo(url, output_dir, ext, quality, is_playlist=False, cookies_opt=None):
    url = fixthatyturl(url)

    quality_map = {
        "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "1080": "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]/best",
        "720": "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best",
        "480": "bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4][height<=480]/best"
    }

    options = maketheoptions(
        output_dir,
        is_playlist,
        cookies_opt
    )

    options["format"] = quality_map.get(
        quality,
        quality_map["best"]
    )

    if ext != "mp4":
        options["postprocessors"] = [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": ext
        }]
    else:
        options["merge_output_format"] = "mp4"

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def howgoodyouwantit():
    print()
    print("Video quality")
    print()
    print("  [1] Best available")
    print("  [2] 1080p")
    print("  [3] 720p")
    print("  [4] 480p")
    print()

    choice = input("Choice: ").strip()

    return {
        "1": "best",
        "2": "1080",
        "3": "720",
        "4": "480"
    }.get(choice, "best")

def whatvideotype():
    print()
    print("Video format")
    print()
    print("  [1] MP4")
    print("  [2] WEBM")
    print("  [3] MKV")
    print()

    choice = input("Choice: ").strip()

    return {
        "1": ("mp4", True),
        "2": ("webm", True),
        "3": ("mkv", True)
    }.get(choice)

def whataudiotype():
    print()
    print("Audio format")
    print()
    print("  [1] MP3")
    print("  [2] WAV")
    print("  [3] FLAC")
    print("  [4] M4A")
    print()

    choice = input("Choice: ").strip()

    return {
        "1": "mp3",
        "2": "wav",
        "3": "flac",
        "4": "m4a"
    }.get(choice)

def singleorplaylistlol(name):
    print()
    print(f"{name} ")
    print()
    print("  [1] Single")
    print("  [2] Playlist")
    print()
    return input("Choice: ").strip() == "2"

def youtubestupidocoglionehahaha():
    cleartheshit()
    makeitlookcool("youtubo maremma trrrrrroia", 0.5)
    print()

    is_playlist = singleorplaylistlol("YouTube")

    print()
    url = input("URL: ").strip()

    if not url:
        return

    cookies_opt = cookiesidk()
    output_dir = putitthere("YouTube")

    print()
    print("Media type")
    print()
    print("  [1] Video")
    print("  [2] Audio")
    print()

    media = input("Choice: ").strip()

    if media == "1":
        selected = whatvideotype()

        if not selected:
            print("Invalid choice.")
            return

        ext, _ = selected
        quality = howgoodyouwantit()

        print()
        print("Downloading...")

        try:
            downloadthatvideo(
                url,
                output_dir,
                ext,
                quality,
                is_playlist,
                cookies_opt
            )

            print()
            print(f"Saved to: {output_dir}")
        except Exception as e:
            print()
            print(f"Error: {type(e).__name__}: {e}")

    elif media == "2":
        codec = whataudiotype()

        if not codec:
            print("Invalid choice.")
            return

        print()
        print("Downloading...")

        try:
            downloadthesong(
                url,
                output_dir,
                codec,
                is_playlist,
                cookies_opt
            )

            print()
            print(f"Saved to: {output_dir}")
        except Exception as e:
            print()
            print(f"Error: {type(e).__name__}: {e}")

    else:
        print("Invalid choice.")

def youtubemusicblahblfefefok32r():
    cleartheshit()
    makeitlookcool("", 0.5)
    print()

    is_playlist = singleorplaylistlol("YouTube Music")

    print()
    url = input("URL: ").strip()

    if not url:
        return

    cookies_opt = cookiesidk()
    output_dir = putitthere("YouTube Music")
    codec = whataudiotype()

    if not codec:
        print("Invalid choice.")
        return

    print()
    print("Downloading...")

    try:
        downloadthesong(
            url,
            output_dir,
            codec,
            is_playlist,
            cookies_opt
        )

        print()
        print(f"Saved to: {output_dir}")
    except Exception as e:
        print()
        print(f"Error: {type(e).__name__}: {e}")

def souncloudblahblfefefok32r():
    cleartheshit()
    makeitlookcool("", 0.5)
    print()

    is_playlist = singleorplaylistlol("SoundCloud")

    print()
    url = input("URL: ").strip()

    if not url:
        return

    output_dir = putitthere("    SoundCloud")
    codec = whataudiotype()

    if not codec:
        print("Invalid choice.")
        return

    print()
    print("Downloading...")

    try:
        downloadthesong(
            url,
            output_dir,
            codec,
            is_playlist
        )

        print()
        print(f"Saved to: {output_dir}")
    except Exception as e:
        print()
        print(f"Error: {type(e).__name__}: {e}")

def whattodownloadlol():
    cleartheshit()
    makeitlookcool("             Risk", 1.1)

    print()
    print("  ")
    print()

    print("  ┌─────────────────────────┐")
    print("  │  [1] YouTube            │")
    print("  │  [2] YouTube Music      │")
    print("  │  [3] SoundCloud         │")
    print("  ├─────────────────────────┤")
    print("  │  [4] Update yt-dlp      │")
    print("  │  [0] Exit               │")
    print("  └─────────────────────────┘")
    print()

def startthisshit():
    while True:
        whattodownloadlol()
        choice = input("  Choice: ").strip()

        if choice == "0":
            cleartheshit()
            makeitlookcool(
                "vaffanculo stupido coglione",
                1.2
            )
            break
        elif choice == "1":
            youtubestupidocoglionehahaha()
        elif choice == "2":
            youtubemusicblahblfefefok32r()
        elif choice == "3":
            souncloudblahblfefefok32r()
        elif choice == "4":
            updatethisstupidthing()
        else:
            print()
            print("  Invalid choice.")

        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    startthisshit()
