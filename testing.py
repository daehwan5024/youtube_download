import pytube.exceptions
from pytube import Playlist
from pytube import YouTube

is_playlist = True
is_single_vid = False

def get_full_link(video_id: str):
    return 'https://www.youtube.com/watch?v='+video_id

link = 'https://www.youtube.com/watch?v=fCO7f0SmrDc&list=RDCLAK5uy_k27uu-EtQ_b5U2r26DNDZOmNqGdccUIGQ&start_radio=1&rv=PYNvQIJ2cuM'
playlist = Playlist(link)
download_id_list = []

try:
    for youtube_vid in playlist.videos:
        download_id_list.append(youtube_vid.video_id)
except KeyError:
    is_playlist = False
    is_single_vid = True
    try:
        youtube_vid = YouTube(link)
        download_id_list.append(youtube_vid.video_id)
    except pytube.exceptions.RegexMatchError:
        print('invalid link')
for vid_id in download_id_list:
    print(get_full_link(vid_id))
