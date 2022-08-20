import tkinter as tk
import os
import spotipy
from time import sleep
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch    
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox


class MainWindow:
    def __init__(self, root):
        root.geometry("876x674")
        root.title("Spotify Playlist Downloader")
        root.config(bg = "#1F1F1F")
        root.resizable(0, 0)
        root.iconbitmap("assets\Spotify_downloader_logo.ico")
        
        title = Label(root, text = "Spotify Playlist Downloader", bg = "#1F1F1F", font = ("System", 30), fg = "White")
        title.pack(pady = 40)
        
        c_id_label = Label(root, text = "Client ID", bg = "#1F1F1F", font = ("System", 18), fg = "White")
        c_id_label.place(x = 222, y = 170)
        
        c_id_entry = Entry(root, font=("System", 10), bg = "White", fg = "#161616")
        c_id_entry.place(x = 155, y = 220, width = 270, height = 22)
                
        c_secret_label = Label(root, text = "Client Secret", bg = "#1F1F1F", font = ("System", 18), fg = "White")
        c_secret_label.place(x = 484, y = 170)
        
        c_secret_entry = Entry(root, font=("System", 10), bg = "White", fg = "#161616")
        c_secret_entry.place(x = 451, y = 220, width = 270, height = 22)
        
        username_label = Label(root, text = "Username", bg = "#1F1F1F", font = ("System", 18), fg = "White")
        username_label.place(x = 370, y = 295)
        
        username_entry = Entry(root, font=("System", 10), bg = "White", fg = "#161616")
        username_entry.place(x = 245, y = 350, width = 400, height = 22)
        
        url_label = Label(root, text = "Playlist URL", bg = "#1F1F1F", font = ("System", 18), fg = "White")
        url_label.place(x = 350, y = 400)
        
        url_entry = Entry(root, font=("System", 10), bg = "White", fg = "#161616")
        url_entry.place(x = 135, y = 450, width = 600, height = 22)
        
        download_button = Button(root, text = "Download", font = ("System", 18), fg = "White", bg = "#1F1F1F", bd = 5, cursor = "hand2", command = lambda: [download_playlist(c_id_entry.get(), c_secret_entry.get(), url_entry.get(), username_entry.get())])
        download_button.place(x = 350, y = 530)


#Get directory to save files
def get_dir():
    directory = filedialog.askdirectory()
    
    if directory != "":
        os.chdir(directory)
        
    return directory


#Get Youtbe video URL
def get_url(song_title):
    
    videosearch = VideosSearch(song_title, limit = 1)
    
    for i in range(1):
        url = (videosearch.result()['result'][i]['link'])
        
    return url


def download_yt_mp3(urls, directory):
    
    for url in urls:
        yt = YouTube(url)
        
        print("\nDownloading:", yt.title, "in mp3...")
        
        output_file = yt.streams.filter(only_audio = True).first()
        download_file = output_file.download(output_path = directory)
        str(download_file)
        base, extensión = os.path.splitext(download_file)
        nuevo_archivo = base + ".mp3"
        os.rename(download_file, nuevo_archivo)

    messagebox.showinfo(message = "Download finished!", title = "Info")


def download_playlist(c_id, c_secret, pl_id, user):
    
    direc = get_dir()
    
    sp = spotipy.Spotify()
    client_credentials_manager = SpotifyClientCredentials(client_id = c_id, client_secret = c_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    sp.trace = False
    
    playlist = sp.user_playlist(user, pl_id, fields = "tracks,next")
    tracks = playlist["tracks"]
    songs = tracks["items"]
    
    song_names = []    
    
    for i in range(len(songs)):
        s = songs[i]["track"]
        song_title = s["name"] + ", " + s["artists"][0]["name"]
        
        song_names.append(song_title)    

    urls = []

    for song in song_names:
        song = get_url(song)
        urls.append(song)
    
    
    download_yt_mp3(urls, direc)  
    

def main():
    app = tk.Tk()
    window = MainWindow(app)
    
    app.mainloop()


if __name__ == '__main__':
    main()