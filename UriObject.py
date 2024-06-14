import urllib
import posixpath
import os

class UriObject:
    """
    An object to represent a URI
    """
    def __init__(self, uri):
        self.uri = uri
        uri_parts = urllib.parse.urlparse(uri)  
        self.scheme = uri_parts.scheme
        self.domain = uri_parts.hostname
        self.username = uri_parts.username
        self.password = uri_parts.password
        self.address = uri_parts.path  
        self.file = posixpath.basename(uri)
        self.filename = os.path.splitext(self.file)[0]
        self.file_extension = os.path.splitext(self.file)[1]
        if uri_parts.port:
            self.port = uri_parts.port
        elif uri_parts.scheme == "http":
            self.port = 80
        elif uri_parts.scheme == "https":
            self.port = 443
        elif uri_parts.scheme == "ftp":
            self.port = 21
        elif uri_parts.scheme == "sftp":
            self.port = 22

    def __eq__(self, other):
        """
        Compare URIs
        """
        return self.domain == other.domain and self.address == other.address and self.scheme == other.scheme
