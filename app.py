from flask import Flask, render_template, request, send_file, after_this_request, redirect
from urllib.parse import unquote
from pytube import Playlist, YouTube
from time import sleep
from os import path
import os
import shutil
import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

# https://www.youtube.com/playlist?list=PL7_XL8L2PxkolJPc__sZgkAl0_qLQBc-x

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.get("/download")
def download():
    url = unquote(request.args.get("url"))
    
    playlist = Playlist(url)
    print("Got playlist", playlist.title, "data")

    title = slugify(playlist.title)

    streams = []

    for video in playlist.videos:
        # Make sure the data is available, otherwise retry
        while True:
            try:
                streams.append({
                    "stream": video.streams.filter(only_audio=True, mime_type="audio/mp4")[0],
                    "title": slugify(video.title)
                })
                print("Got", video.title, "data")
                break

            except Exception as e:
                print(f"Failed to get video data. Retrying with {video.watch_url}... {e}")
                sleep(1)
                video = YouTube(video.watch_url)
                continue

    for stream_data in streams:
        stream_data.get("stream").download(path.join("downloaded", title), filename=stream_data.get("title") + ".mp3")

    # Package the downloaded songs in a zip archive
    shutil.make_archive(path.join("downloaded", title), "zip", root_dir=path.join("downloaded", title))

    # Clean up by removing the folder
    shutil.rmtree(path.join("downloaded", title))

    

    @after_this_request
    def after_request(response):
        os.remove(path.join("downloaded", title + ".zip"))
        return response
        

    return send_file(path.join("downloaded", title + ".zip"), "application/zip", True)

@app.route("/downloaded")
def downloaded():
    return render_template("downloaded.html")