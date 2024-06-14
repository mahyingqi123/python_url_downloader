import unittest
from HttpDownloader import HttpDownloader
from FtpDownloader import FtpDownloader
from SftpDownloader import SFTPDownloader
import os
from UriObject import UriObject
from UriDownloader import UriDownloader

location = os.getcwd()
uris = {
    "http": "http://speedtest.tele2.net/1MB.zip",
    "ftp": "ftp://demo:password@test.rebex.net/readme.txt",
    "sftp": "sftp://demo:password@test.rebex.net/readme.txt"
}
class TestHttpDownload(unittest.TestCase):
    def test_download(self):
        uri = uris["http"]
        http_downloader = HttpDownloader()
        download_result, message = http_downloader.download(UriObject(uri))
        self.assertEqual(message, f"Downloaded {uri}")
        self.assertNotEqual(download_result, None)

class TestFtpDownload(unittest.TestCase):
    def test_download(self):
        uri = uris["ftp"]
        ftp_downloader = FtpDownloader()
        download_result, message = ftp_downloader.download(UriObject(uri))
        self.assertEqual(message, f"Downloaded {uri}")
        self.assertNotEqual(download_result, None)


class TestSFTPDownload(unittest.TestCase):
    def test_download(self):
        uri = uris["sftp"]
        sftp_downloader = SFTPDownloader()
        download_result, message = sftp_downloader.download(UriObject(uri))
        self.assertEqual(message, f"Downloaded {uri}")
        self.assertNotEqual(download_result, None)

class TestUriDownloader(unittest.TestCase):
    def test_download_http(self):
        uri = uris["http"]
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uri, location, retries)
        self.assertEqual(result, f"Downloaded {uri}\n")
        self.assertTrue(os.path.exists(location + "\\1MB.zip"))
        os.remove(location + "\\1MB.zip")

    def test_download_ftp(self):
        uri = "ftp://test.rebex.net/readme.txt"
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uri, location, retries)
        self.assertEqual(result, "Downloaded ftp://test.rebex.net/readme.txt\n")
        self.assertTrue(os.path.exists(location + "\\readme.txt"))
        os.remove(location + "\\readme.txt")

    def test_download_sftp(self):
        uri = "sftp://demo:password@test.rebex.net/readme.txt"
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uri, location, retries)
        self.assertEqual(result, "Downloaded sftp://demo:password@test.rebex.net/readme.txt\n")
        self.assertTrue(os.path.exists(location + "\\readme.txt"))
        os.remove(location + "\\readme.txt")

    def test_download_multiple(self):
        uris = "http://speedtest.tele2.net/1MB.zip ftp://test.rebex.net/readme.txt sftp://demo:password@test.rebex.net/readme.txt"
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uris, location, retries)
        self.assertIn("Downloaded http://speedtest.tele2.net/1MB.zip",result)
        self.assertIn("Downloaded ftp://test.rebex.net/readme.txt",result)
        self.assertIn("Downloaded sftp://demo:password@test.rebex.net/readme.txt",result)
        self.assertTrue(os.path.exists(location + "\\1MB.zip"))
        self.assertTrue(os.path.exists(location + "\\readme.txt"))
        self.assertTrue(os.path.exists(location + "\\readme_1.txt"))
        os.remove(location + "\\1MB.zip")
        os.remove(location + "\\readme.txt")
        os.remove(location + "\\readme_1.txt")
    
    def test_download_name_clash(self):
        uris = "ftp://test.rebex.net/readme.txt sftp://demo:password@test.rebex.net/readme.txt"
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uris, location, retries)
        self.assertIn("Downloaded ftp://test.rebex.net/readme.txt",result)
        self.assertIn("Downloaded sftp://demo:password@test.rebex.net/readme.txt",result)
        self.assertTrue(os.path.exists(location + "\\readme.txt"))
        self.assertTrue(os.path.exists(location + "\\readme_1.txt"))
        os.remove(location + "\\readme.txt")
        os.remove(location + "\\readme_1.txt")

    def test_download_same_resources(self):
        uris = "http://speedtest.tele2.net/1MB.zip http://speedtest.tele2.net/1MB.zip"
        retries = 2
        uri_extractor = UriDownloader()
        result = uri_extractor.download_uris(uris, location, retries)
        self.assertEqual(result, "Downloaded http://speedtest.tele2.net/1MB.zip\n")
        self.assertTrue(os.path.exists(location + "\\1MB.zip"))
        self.assertFalse(os.path.exists(location + "\\1MB_1.zip"))
        os.remove(location + "\\1MB.zip")
        

if __name__ == '__main__':
    unittest.main()