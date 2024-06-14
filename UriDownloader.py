
import multiprocessing as mp
import posixpath
from SftpDownloader import SFTPDownloader
from FtpDownloader import FtpDownloader
from HttpDownloader import HttpDownloader
from UriObject import UriObject
from multiprocessing import Manager
    
class UriDownloader:
    """
    URIExtractor class is responsible for downloading files from different URIs.
    Currently support HTTP, FTP, and SFTP protocols.

    """
    def __init__(self):
        self.router = {
            "http": HttpDownloader(),
            "https": HttpDownloader(), 
            "ftp": FtpDownloader(),
            "sftp": SFTPDownloader()
        }

    def add_protocol(self, protocol, downloader):
        """
        Add a new protocol to the router
        """
        self.router[protocol] = downloader

    def partition(self, uris, processor_count):
        """
        Partition the URIs into processor_count partitions for parallel download
        """
        result = [[] for i in range(processor_count)]
        for i in range(len(uris)):
            result[i%processor_count].append(uris[i])
        return result

    def search_file_name(self, download_result, location, uri, shared_dict):
        """
        handle name conflict when downloading files
        """
        file_to_write = ""
        if uri.filename not in shared_dict or shared_dict[uri.filename]['uri'] == uri:
            shared_dict[uri.filename] = {'uri':uri}
            file_to_write = uri.filename
        else:
            same_count = 1
            new_filename = uri.filename+'_'+str(same_count)
            while new_filename in shared_dict and  shared_dict[new_filename]['uri'] != uri:
                same_count += 1
                new_filename = uri.filename+'_'+str(same_count)
            shared_dict[new_filename] = {'uri':uri}
            file_to_write = new_filename

        with open(posixpath.join(location, file_to_write+uri.file_extension), 'wb') as f:
            try:
                f.write(download_result)
            except Exception as e:
                pass

                

    def download_uris_partition(self, partition, shared_dict, location, retries):
        """
        Download URIs in a partition
        """
        result = ""
        for uri in partition:
            if uri.scheme in self.router:
                for retry_count in range(int(retries)):
                    try:
                        # download the file using selected downloader
                        download_result, message = self.router[uri.scheme].download(uri)
                        if download_result is not None:
                            self.search_file_name(download_result, location, uri, shared_dict)
                            result += message + "\n"
                            break
                        if retry_count == int(retries) - 1:
                            result += f"Failed to download {uri.uri} after {retry_count+1} retries due to {message}\n"
                    except Exception as e:
                        result += f"Failed to download {uri.uri} due to {e}\n"
            else:
                result += f"Unsupported protocol: {uri.uri}\n"
        return result

    def download_uris(self, uris, locations, retries):
        """
        Download URIs
        """
        uris = list(set(uris.split()))
        uris = [UriObject(uri) for uri in uris]

        cpu_count = mp.cpu_count()

        partitions = self.partition(uris, cpu_count)
        process_result = []

        # create a shared dict to store the downloaded files
        manager = Manager()
        shared_dict = manager.dict()

        pool = mp.Pool(cpu_count)

        # create parallel processes to download the partitions
        for partition in partitions:
            process_result.append(pool.apply_async(self.download_uris_partition, args=([partition,shared_dict, locations, retries])))
        pool.close()
        pool.join()

        result = ""
        # get the result message from the processes
        for r in process_result:
            result += r.get()
        return result


