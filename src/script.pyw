import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, sys
import subprocess
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

#YouTube
def downloadButton():
    try:
        url = ytUrl.get()
        if "list=" in url or "playlist=" in url:
            messagebox.showwarning("Advertencia", "Esta por descargar una Playlist, esto tomara bastante tiempo.")
            p = Playlist(url)
            for v in p.videos:
                download(v.watch_url)
        else:
            download(url)
        messagebox.showinfo("Completado", "Descarga completada!")
    except Exception as e:
        messagebox.showerror("Error", e)

def download(url):
    try:
        yt = YouTube(url)
        if(ytSaveType.current()==0):
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=dirEntry.get())
        else:
            stream = yt.streams.get_audio_only()
            inputFile = stream.download(output_path = dirEntry.get(), filename = 'temp.mp4')
            outputFile = dirEntry.get() + "/" + stream.default_filename.replace(".mp4", ".mp3")
            subprocess.run(['ffmpeg', '-i', inputFile, outputFile], check=True)
            os.remove(inputFile)
    except RegexMatchError as rme:
        messagebox.showerror("Error", "El enlace no es valido.")
    except Exception as e:
        messagebox.showerror("Error", e)

#Path
#Get Defaulth Path:
path = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(path):
    path = filedialog.askdirectory()

#Select Path:
def select_path():
    path = filedialog.askdirectory()
    if(path!=""):
        dirEntry.config(state = tk.NORMAL)
        dirEntry.delete(0, tk.END)
        dirEntry.insert(0, path)
        dirEntry.config(state = tk.DISABLED)

#TK
root = tk.Tk()
root.title("Simple YT Downloader")
root.resizable(False, False)
try:
    root.iconbitmap("icon.ico")
except:
    pass

title = tk.Label(root, text = "[Simple YT Downloader]")
title.pack(pady = 10)

#Directory
dirFrame = tk.Frame(root)
dirFrame.pack()

dirEntry = tk.Entry(dirFrame, width = 50)
dirEntry.grid(row = 0, column = 0, padx = [0,10])
dirEntry.insert(0, path)
dirEntry.config(state = tk.DISABLED)

dirButton = tk.Button(dirFrame, text = "📁", command = select_path)
dirButton.grid(row = 0, column = 1)

#Youtube
ytFrame = tk.Frame(root)
ytFrame.pack(padx = 20, pady = 10)

ytSaveType = ttk.Combobox(ytFrame, width = 5, values = ["video", "audio"], state = "readonly")
ytSaveType.grid(row = 0, column = 0)
ytSaveType.current(0)

ytUrl = tk.Entry(ytFrame, width = 50)
ytUrl.grid(row = 0, column = 1, padx = 10)

ytDownload = tk.Button(ytFrame, text = "📥", command = downloadButton)
ytDownload.grid(row = 0, column = 2)

credits_ = tk.Label(root, text = "(b3ll_4rt, python, pytube, ffmpeg)")
credits_.pack(pady = [0,10])

root.mainloop()
