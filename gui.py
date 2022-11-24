import tkinter as tk
import tkinter.messagebox as messagebox
import threading
import os

import pytube.exceptions
from pytube import YouTube
from pytube import Search
from pytube import Playlist

youtube_vid_dict = {}
selected_index = []
on_selection_window = False


class LoadingWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(main_window)
        self.title('찾는중')
        self.protocol('WM_DELETE_WINDOW', self.nothing)
        self.geometry('150x150')
        self.label = tk.Label(self, text='동영상 가져오는 중')
        self.label.pack()

    def nothing(self):
        pass


class SearchingWindow(tk.Toplevel):
    def __init__(self, youtube_search:pytube.Search):
        global on_selection_window
        on_selection_window = True
        super().__init__(main_window)
        self.title('영상 선택')
        self.geometry('400x400')
        self.youtube_search = youtube_search
        self.y_scrollbar = tk.Scrollbar(self)
        self.y_scrollbar.pack(side="right", fill="y")
        self.x_scrollbar = tk.Scrollbar(self, orient='horizontal')
        self.x_scrollbar.pack(side='bottom', fill='x')
        self.download_list = tk.Listbox(self, selectmode="extended", height=15,
                                        yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.download_list.pack(side="left", fill="both", expand=True)
        self.y_scrollbar.config(command=download_list.yview)
        self.x_scrollbar.config(command=download_list.xview)
        self.set_videos()

        self.confirm_button = tk.Button(self, text='확인', command=self.on_click)
        self.confirm_button.pack()

    def on_click(self):
        global selected_index, on_selection_window
        selected_index = []
        for items in self.download_list.curselection():
            selected_index.append(items)
        on_selection_window = False
        self.destroy()

    def destroy(self) -> None:
        super().destroy()
        global on_selection_window
        on_selection_window = False

    def set_videos(self):
        for vid in self.youtube_search.results:
            self.download_list.insert(tk.END, vid.title)


def search():
    youtube_vid: YouTube
    playlist: Playlist
    search_youtube: Search
    is_vid = False
    is_playlist = False
    is_search = False
    link = youtube_link_input_entry.get()
    loading_window = LoadingWindow()
    loading_window.update()
    try:
        playlist = Playlist(link)
        try:
            if len(playlist.videos) == 0:
                messagebox.showerror('에러', '플레이리스트에서 동영상을 가져올 수 없습니다')
                print('no video in playlist')
            else:
                is_search, is_vid, is_playlist = False, False, True
        except KeyError:
            youtube_vid = YouTube(link)
            is_search, is_vid, is_playlist = False, True, False
    except pytube.exceptions.RegexMatchError:
        is_search, is_vid, is_playlist = True, False, False
        search_youtube = Search(link)
        print('going to use search')
    loading_window.destroy()

    if is_vid:
        vid_name = youtube_vid.title
        if vid_name in youtube_vid_dict:
            messagebox.showerror('error', '이미 존재하는 동영상입니다.')
            return
        youtube_vid_dict[vid_name] = youtube_vid
        download_list.insert(tk.END, vid_name)
        main_window.update()
    elif is_playlist:
        for vid in playlist.videos:
            vid_name = vid.title
            if vid_name in youtube_vid_dict:
                continue
            print(vid_name)
            youtube_vid_dict[vid_name] = vid
            download_list.insert(tk.END, vid_name)
            main_window.update()
    elif is_search:
        searching_window = SearchingWindow(search_youtube)
        while on_selection_window:
            searching_window.update()
        print(selected_index)
        for result in search_youtube.results:
            vid_name = result.title
            print(vid_name)


# main window
main_window = tk.Tk()
main_window.geometry('500x500')
main_window.wm_title('youtube downloader')
main_window.iconbitmap(default='youtube.ico')

# link input frame
link_frame = tk.LabelFrame(main_window, text='유튜브 링크')
link_frame.pack(fill='x', padx=5, pady=5, ipady=5)
youtube_link_input_entry = tk.Entry(link_frame)
youtube_link_input_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5, ipady=5)
link_confirm_button = tk.Button(link_frame, text='찾아보기', command=search)
link_confirm_button.pack(side='right', fill='x', expand=False, padx=5, pady=5, ipady=5)

# videos to download
list_frame = tk.Frame(main_window)
list_frame.pack(fill="both", padx=5, pady=5)
y_scrollbar = tk.Scrollbar(list_frame)
y_scrollbar.pack(side="right", fill="y")
x_scrollbar = tk.Scrollbar(list_frame, orient='horizontal')
x_scrollbar.pack(side='bottom', fill='x')
download_list = tk.Listbox(list_frame, selectmode="extended", height=15,
                           yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
download_list.pack(side="left", fill="both", expand=True)
y_scrollbar.config(command=download_list.yview)
x_scrollbar.config(command=download_list.xview)

# start the program
main_window.mainloop()
