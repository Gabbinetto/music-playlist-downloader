from flask import Flask, render_template, request, send_file, after_this_request, redirect
from urllib.parse import unquote
from pytube import Playlist, YouTube
from time import sleep
from os import path
from moviepy.editor import VideoFileClip
from typing import Dict, List
from utils import slugify, caption_string
import eyed3
import os
import time
import shutil
import subprocess
import urllib.request

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('index.html')


@app.get("/download")
def download():
    url = unquote(request.args.get("url"))

    playlist = Playlist(url)
    print("Got playlist", playlist.title, "data. Lenght: ", playlist.length)

    title = str(time.time())  # slugify(playlist.title)

    streams: List[Dict] = []

    for i, video in enumerate(playlist.videos):
        # Make sure the data is available, otherwise retry

        while True:
            try:
                streams.append({
                    "stream": video.streams.filter(mime_type="video/mp4")[0],
                    "title": slugify(video.title),
                    "raw_title": video.title,
                    "artist": video.author,
                    "index": i + 1,
                    "thumbnail": video.thumbnail_url,
                    "video_id": video.video_id
                })
                print("Got", video.title, "data")
                break

            except Exception as e:
                print(
                    f"Failed to get video data. Retrying with {video.watch_url}...\n{e}")
                sleep(1)
                video = YouTube(video.watch_url)
                continue

    for stream_data in streams:

        stream_data.get("stream").download(
            path.join("downloaded", title), filename=stream_data.get("title") + ".mp4")
        video_file = VideoFileClip(
            path.join("downloaded", title, stream_data.get("title") + ".mp4"))
        video_file.audio.write_audiofile(
            path.join("downloaded", title, stream_data.get("title") + ".mp3"))
        os.remove(path.join("downloaded", title,
                  stream_data.get("title") + ".mp4"))

        if request.args.get("metadata", None) == "true":
            while not path.exists(path.join("downloaded", title, stream_data.get("title") + ".mp3")):
                print("File", stream_data.get("title"),
                      "does not exist, retrying...")
                sleep(0.5)
                continue

            audiofile = eyed3.load(
                path.join("downloaded", title, stream_data.get("title") + ".mp3"))

            audiofile.initTag(version=(2, 3, 0))

            if audiofile:
                while True:
                    try:
                        audiofile.tag.title = stream_data.get("raw_title")
                        audiofile.tag.artist = stream_data.get("artist")
                        audiofile.tag.album = playlist.title
                        audiofile.tag.album_artist = playlist.owner
                        audiofile.tag.track_num = (
                            stream_data.get("index"), playlist.length)
                        print("Set ID3 tags")

                        thumbnail = urllib.request.urlopen(
                            stream_data.get("thumbnail"))
                        imagedata = thumbnail.read()
                        audiofile.tag.images.set(
                            3, imagedata, "image/jpeg", u"cover")
                        print("Set ID3 cover tag")

                        # lyrics = caption_string(stream_data.get("video_id"))
                        # file_name = str(time.time()) + ".txt"
                        # with open(file_name, "w") as lyrics_file:
                        #     lyrics_file.write(lyrics)

                        # sleep(0.2)
                        # subprocess.run(
                        #     f"eyeD3 {path.join('.', 'downloaded', title, stream_data.get('title') + '.mp3')} --add-lyrics {file_name}"
                        # )
                        # os.remove(file_name)
                        # print("Added ID3 Lyrics")

                        audiofile.tag.save()

                        break

                    except Exception as e:
                        print("Failed to load", stream_data.get(
                            "title"), "file, retrying...")
                        print("Exception: ", e)
                        sleep(1)
                        audiofile = eyed3.load(
                            path.join("downloaded", title, stream_data.get("title") + ".mp3"))
                        continue
            else:
                raise Exception("Audiofile is None")

    # Package the downloaded songs in a zip archive
    shutil.make_archive(path.join("downloaded", slugify(
        playlist.title)), "zip", root_dir=path.join("downloaded", title))

    # Clean up by removing the folder
    shutil.rmtree(path.join("downloaded", title))

    @after_this_request
    def after_request(response):
        os.remove(path.join("downloaded", title + ".zip"))
        return response

    return send_file(path.join("downloaded", title + ".zip"), "application/zip", True)
