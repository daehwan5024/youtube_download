import os
import subprocess
from pytube import YouTube as Video
from pytube import Playlist
from pytube import Channel
from pytube import Search


def clear_console():  # Clears the console
    os.system("cls" if os.name == "nt" else "clear")


# Validates the file name to avoid some errors
def file_name_validation(file_name):
    INVALID_CHARACTERS = {"|", "/", "\\", ":", "*", "?", "<", ">", '"'}

    for char in INVALID_CHARACTERS:
        file_name = file_name.replace(char, "")

    return file_name


def create_video_audio_path(video):  # Creates the path for the video or audio
    path = file_name_validation(video.title)
    return path


def create_channel_path(channel):  # Creates the path for the channel
    path = file_name_validation(channel.channel_name)
    return path


def create_playlist_path(playlist):  # Creates the path for the playlist
    path = file_name_validation(playlist.title)
    return path


def search_video(search_input):  # Search for a video
    video_num = 1
    results = Search(search_input)
    clear_console()
    print(f"\nWe found {len(results.results)} results for: {search_input}\n")
    for result in results.results:
        print(f"{video_num} - {result.title}")
        video_num += 1
    try:
        selected_video = int(input("\nSelect a video to download: "))
    except Exception:
        not_found("video")
    video_to_download = results.results[selected_video - 1]
    print(f"\nSelected video: {video_to_download.title}")
    video_id = str(video_to_download)
    video_id = video_id.replace(
        "<pytube.__main__.YouTube object: videoId=", "")
    video_id = video_id.replace(">", "")
    video_link = f"https://www.youtube.com/watch?v={video_id}"
    return video_link


def on_complete(stream, file_path):  # When the single video is downloaded
    print(f"\n\nSuccesfully downloaded {file_path}")
    if os.name == "nt":  # If the OS is Windows
        subprocess.Popen(fr'explorer /select,"{file_path}"')


# When the playlist video is downloaded
def playlist_video_on_complete(stream, downloaded_playlist_video_title):
    print(f"\nDownloaded {downloaded_playlist_video_title}")


# Opens the file path of the playlist
def open_playlist_file_path(playlist_to_download, video_in_playlist, to_download):
    if os.name == "nt":  # If the OS is Windows
        if to_download == "v":  # If the video is selected
            path = f"{playlist_to_download.title}\{video_in_playlist.title}.mp4"
            subprocess.Popen(fr'explorer /select,"{path}"')
        elif to_download == "a":  # If the audio is selected
            try:
                path = f"{playlist_to_download.title}\{video_in_playlist.title}.webm"
            except Exception:
                path = f"{playlist_to_download.title}\{video_in_playlist.title}.wav"
            subprocess.Popen(fr'explorer /select,"{path}"')


# Opens the file path of the channel
def open_channel_file_path(channel_to_download, video_in_channel, to_download):
    if os.name == "nt":
        if to_download == "v":
            path = f"{channel_to_download.channel_name}\{video_in_channel.title}.mp4"
            subprocess.Popen(fr'explorer /select,"{path}"')
        elif to_download == "a":
            try:
                path = f"{channel_to_download.channel_name}\{video_in_channel.title}.webm"
            except Exception:
                path = f"{channel_to_download.channel_name}\{video_in_channel.title}.wav"
            subprocess.Popen(fr'explorer /select,"{path}"')


# Prints the download progress
def view_download_progress(stream, chunk, bytes_remaining):
    percent = (1 - bytes_remaining / stream.filesize) * 100
    print(str(percent), end="")


def not_found(type):
    if(type == "video"):  # If the video is not found
        print("\nVideo was not found")
    elif(type == "playlist"):  # If the playlist is not found
        print("\nPlaylist was not found")
    elif(type == "channel"):  # If the channel is not found
        print("\nChannel was not found")
    else:
        print("\nVideo, channel or playlist was not found")
    exit()


def choose_video_quality():  # Define the video quality and download
    quality = input(
        "\nChoose the quality of video:\nBest(b) | Worst(w)\nchoice: ").lower()
    if quality == "b":  # Best quality
        print("\nDownloading...")
        if mode == "v" or mode == "s":  # Single video
            try:
                video_to_download.streams.get_by_itag(22).download(  # 720p youtube video itag. 1080p videos come without audio
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_highest_resolution().download(  # Highest video quality available
                    create_video_audio_path(video_to_download))
        elif mode == "p":  # Playlist
            opened_file_path = False  # To check if the file path was opened
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(22).download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:  # If the file path was not opened
                        # Define that the file path was opened to avoid opening it again and again when the video is downloaded
                        opened_file_path = True
                        # Open the file path of the playlist
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
                except Exception:
                    video_in_playlist.streams.get_highest_resolution().download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
        elif mode == "c":  # Channel
            opened_file_path = False
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(22).download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)
                except Exception:
                    video_in_channel.streams.get_highest_resolution().download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)
    elif quality == "w":  # Worst quality
        print("\nDownloading...")
        if mode == "v" or mode == "s":  # Single video
            video_to_download.streams.get_lowest_resolution().download(  # 360p youtube video
                create_video_audio_path(video_to_download))
        elif mode == "p":  # Playlist
            opened_file_path = False
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                video_in_playlist.streams.get_lowest_resolution().download(
                    create_playlist_path(playlist_to_download))
                if opened_file_path == False:
                    opened_file_path = True
                    open_playlist_file_path(
                        playlist_to_download, video_in_playlist, to_download)
        elif mode == "c":  # Channel
            opened_file_path = False
            for video_in_channel in channel_to_download.videos:
                video_in_channel.streams.get_lowest_resolution().download(
                    create_channel_path(channel_to_download))
                if opened_file_path == False:
                    opened_file_path = True
                    open_channel_file_path(
                        channel_to_download, video_in_channel, to_download)
    else:
        print("Invalid choice")


def choose_audio_quality():  # Define the audio quality and download
    quality = input(
        "\nChoose the quality of audio:\nBest(b) | Worst(w)\nchoice: ").lower()
    if quality == "b":  # Best quality
        print("\nDownloading...")
        if mode == "v" or mode == "s":  # Single video
            try:
                video_to_download.streams.get_by_itag(251).download(  # only audio itag, 160kbps
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_audio_only().download(  # only audio itag, 160kbps
                    create_video_audio_path(video_to_download))
        elif mode == "p":  # Playlist
            opened_file_path = False
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(251).download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
                except Exception:
                    video_in_playlist.streams.get_audio_only().download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
        elif mode == "c":  # Channel
            opened_file_path = False
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(251).download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)
                except Exception:
                    video_in_channel.streams.get_audio_only().download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)
    elif quality == "w":  # Worst quality
        print("\nDownloading...")
        if mode == "v" or mode == "s":  # Single video
            try:
                video_to_download.streams.get_by_itag(249).download(  # only audio itag, 50kbps
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_by_itag(250).download(  # only audio itag, 70kbps
                    create_video_audio_path(video_to_download))
        elif mode == "p":  # Playlist
            opened_file_path = False
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(249).download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
                except Exception:
                    video_in_playlist.streams.get_by_itag(250).download(
                        create_playlist_path(playlist_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_playlist_file_path(
                            playlist_to_download, video_in_playlist, to_download)
        elif mode == "c":  # Channel
            opened_file_path = False
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(249).download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)
                except Exception:
                    video_in_channel.streams.get_by_itag(250).download(
                        create_channel_path(channel_to_download))
                    if opened_file_path == False:
                        opened_file_path = True
                        open_channel_file_path(
                            channel_to_download, video_in_channel, to_download)


def download():  # Init the download and quality options for the mode selected
    if to_download == "v":
        choose_video_quality()
    elif to_download == "a":
        choose_audio_quality()
    else:
        print("Invalid choice")


mode = input(
    "\nSelect the mode:\nVideo(v) | Playlist/Playlist video(p) | Channel(c) | Search video(s)\nchoice: ").lower()


if mode == "v":  # Video mode
    link = input("\nEnter the link of the video: ")
elif mode == "p":  # Playlist mode
    link = input("\nEnter the link of the playlist: ")
elif mode == "c":  # Channel mode
    link = input("\nEnter the link of the channel: ")
elif mode == "s":  # Search mode
    search = input("\nEnter the search: ")
    link = search_video(search)
else:
    print("\nInvalid mode")
    exit()

if mode == "v" or mode == "s":  # Single video mode
    try:
        video_to_download = Video(
            link, on_complete_callback=on_complete, on_progress_callback=view_download_progress, use_oauth=False, allow_oauth_cache=True)
    except Exception:
        not_found("video")
elif mode == "p":  # Playlist mode
    try:
        playlist_to_download = Playlist(link)
    except Exception:
        not_found("playlist")
elif mode == "c":  # Channel mode
    try:
        channel_to_download = Channel(link)
    except Exception:
        not_found("channel")

if mode == "v" or mode == "s":  # Single video mode. Get the video informations
    clear_console()
    print(f"\nTitle: {video_to_download.title}")
    print(f"Thumbnail: {video_to_download.thumbnail_url}")
    print(f"Views: {video_to_download.views}")
    print(f"Duration: {round(video_to_download.length / 60,2)}")
elif mode == "p":  # Playlist mode. Get the playlist informations
    clear_console()
    print(f"\nPlaylist title: {playlist_to_download.title}")
    print(f"Playlist views: {playlist_to_download.views}")
    print(f"{len(playlist_to_download.videos)} videos on playlist to download")
elif mode == "c":  # Channel mode. Get the channel informations
    clear_console()
    print(
        f"\nChannel to download all videos: {channel_to_download.channel_name}")

to_download = input(
    "\nOptions available:\nVideo(v) | Audio(a)\nchoice: ").lower()

try:
    download()
except Exception:
    print("YouTube is experiencing some problems. Please try again later")

print("\nAll done")
