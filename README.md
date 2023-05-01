# Music playlist downloader

Ever needed to download your YouTube playlist as music? This is the tool you need. Just input the playlist link and download.

## Requirements
* Python 3.10+
* Flask
* Pytube
* MoviePy
* EyeD3

## Usage

* Clone the repository (You can also [download the repository as a zip file](https://github.com/Gabbinetto/music-playlist-downloader/archive/refs/heads/master.zip))
    ```
    git clone https://github.com/Gabbinetto/music-playlist-downloader.git
    ```
* Navigate to the directory and run the Flask app
    ```
    flask run
    ```
    You can use this on another device connected to the same network with
    ```
    flask run --host=0.0.0.0
    ```
* Connect to the ip address shown, which may be `localhost:5000` or other LAN addresses.

You can also host your own server or use hosting services like [PythonAnywhere](https://www.pythonanywhere.com/).

## Credits
Myself and Pytube and Flask which made this possible.
