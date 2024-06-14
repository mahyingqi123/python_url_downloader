import paramiko

class SFTPDownloader:
    """
    Downloader to download files from SFTP
    """
    def download(self, uri):
        result = ""
        message = ""
        try:
            transport = paramiko.Transport((uri.domain, uri.port))
            transport.connect(username=uri.username, password=uri.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            result = sftp.open(uri.address,'r').read()
            sftp.close()
            transport.close()
            message=f"Downloaded {uri.uri}"
        except Exception as e:
            result = None
            message = str(e)
        return result, message