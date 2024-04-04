import os
import asyncio
from pyrogram import Client, filters
import yt_dlp  # Use yt-dlp instead of youtube_dl

BOT_TOKEN = "YOUR_BOT_TOKEN"
DOWNLOAD_DIR = "downloads"

app = Client("url_downloader_bot", bot_token=BOT_TOKEN)

async def download_url(client, message):
    url = message.text.split()[1]  # Extract URL from message (assuming format "/download <URL>")

    # Error handling for invalid URLs
    try:
        ydl_opts = {
            "format": "best",  # Download best available format
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),  # Output filename template
            "postprocessors": [{
                "key": "FFmpegExtractAudio",  # Optionally extract audio only
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "external_downloader": "aria2c",  # Use aria2c for downloads
            "quiet": True,  # Suppress yt-dlp output messages
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)

            # Send download progress updates (optional)
            # async def download_progress(d):
            #     if d['status'] == 'downloading':
            #         progress = d['_percent_str']
            #         await message.reply_text(f"Downloading: {progress}")

            # ydl.add_progress_callback(download_progress)

            try:
                ydl.download([url])
                await message.reply_text(f"Downloaded: {filename}")
            except Exception as e:
                await message.reply_text(f"Download failed: {str(e)}")

    except Exception as e:
        await message.reply_text(f"Invalid URL: {str(e)}")

@app.on_message(filters.command(["download"]))
async def download_command(client, message):
    await download_url(client, message)

asyncio.get_event_loop().run_until_complete(app.run())
