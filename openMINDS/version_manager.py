import os
import git
import urllib3
import tempfile
import pathlib
import zipfile

class Version_Manager:

    def download(self, version_name, url):
        http = urllib3.PoolManager()
        #response = http.request('GET', self.versions["v1.0.0"])
        response = http.request('GET', url)
        datatowrite = response.data
        print(datatowrite)

        download_folder = self.cache_dir + "/" + version_name + "/"
        pathlib.Path(download_folder).mkdir(parents=True, exist_ok=True)

        download_file = download_folder + version_name + ".zip"

        with open(download_file, 'wb+') as f:
            f.write(datatowrite)

        return (download_folder, download_file)


    def extract(self, folder, file_name):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(folder)


    def download_and_extract(self):
        for version in self.versions:
            version_download = self.download(version, self.versions[version]["url"])
            self.extract(version_download[0], version_download[1])


    def __init__(self):
        home = str(pathlib.Path.home())
        self.cache_dir = home + "/.openMINDS"
        pathlib.Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

        self.versions = {
            "dev": {
                "url": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/dev.zip",
                "core": "dev/schema.json/core/schemas/v3"
                },
            "v1.0.0": {
                "url": "https://github.com/HumanBrainProject/openMINDS/releases/download/v1.0.0/openMINDS_v1.0.0.zip",
                "core": "v1.0.0/core/v3/schema.json"
                }
        }

        self.download_and_extract()
