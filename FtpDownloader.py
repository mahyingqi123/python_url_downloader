import urllib.request

class FtpDownloader:
    """
    Downloader for FTP protocol
    """
    def download(self, uri):
        result = ""
        message = ""
        try:
            with urllib.request.urlopen(uri.uri) as response:
                data = response.read()
            result = data
            message = f"Downloaded {uri.uri}"
        except Exception as e:
            result = None
            message = str(e)
        return result, message