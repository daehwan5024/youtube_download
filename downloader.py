import os
import subprocess
import pytube
from pytube import request
from pytube import YouTube
from pytube import Search
link = 'https://www.youtube.com/watch?v=iTK3E1zooRY'
request.default_range_size = 1024*1024*9


def to_appropriate_size(file_size: int):
    in_kb = file_size/1024
    in_mb = in_kb/1024
    in_gb = in_mb/1024
    if in_kb < 1024:
        return str(in_kb)+'kb'
    elif in_mb < 1024:
        return str(in_mb)+'mb'
    else:
        return str(in_gb)+'gb'


def on_complete(stream, file_path):
    print(to_appropriate_size(stream.filesize))


def view_download_progress(stream, chunk, bytes_remaining):
    print((stream.filesize-bytes_remaining)/stream.filesize)


if __name__ == '__main__':
    youtube_vid = YouTube(link, on_complete_callback=on_complete, on_progress_callback=view_download_progress,
                          use_oauth=False, allow_oauth_cache=False)
    print('starting download')
    youtube_vid.streams.get_highest_resolution().download()
    print('download done')
