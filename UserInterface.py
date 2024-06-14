from tkinter import filedialog
import tkinter.messagebox
import tkinter as tk
from UriDownloader import UriDownloader
class UI:
    """
    UI class is responsible for the user interface of the URI downloader
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("URI Extractor")
        self.root.geometry("500x550")
        self.result = ""
        
    def run(self):
        instruction = tk.Label(text="Enter the URIs", pady=10, font=("Helvetica", 16))
        instruction.pack()
        information = tk.Label(text="Supported protocols: http, https, ftp, sftp.\n\n HTTP/HTTPS format: 'http://hostname/path/to/file' \n FTP format: 'ftp://[username[:password]@]hostname[:port]/path/to/file'\n SFTP format: 'sftp://[username[:password]@]hostname[:port]/path/to/file'\n\nPlease separate each URI by space or newline", pady=10)
        information.pack()
        text = tk.Text(width=50, height=10, )
        text.pack()

        instruction2 = tk.Label(text="Enter the download location", pady=10)
        instruction2.pack()

        location = tk.Entry()
        location.pack()

        location_button = tk.Button(text="Browse", command=lambda: location.insert(0, filedialog.askdirectory()))
        location_button.pack()

        instruction3 = tk.Label(text="Enter the number of retries", pady=10)
        instruction3.pack()

        retries = tk.Entry()
        retries.pack()

        submit = tk.Button(text="Submit", command=lambda: self.uri_download(text.get("1.0", tk.END), location.get(), retries.get()))
        submit.pack()

        self.root.mainloop()
    
    def uri_download (self, uris, location, retries):
        downloader = UriDownloader()
        result = downloader.download_uris(uris, location, retries)
        tkinter.messagebox.showinfo("Download Result", result)

