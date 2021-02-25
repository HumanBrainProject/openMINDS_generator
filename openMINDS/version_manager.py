import os
import git
import urllib3
import tempfile
import pathlib
import zipfile

class Version_Manager:

    def download(self, version_name, url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        datatowrite = response.data

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
                "core": "dev/schema.json/core/schemas/v3",
                "sands": "dev/schema.json/SANDS/schemas/v1"
            },
            "v1.0.0": {
                "url": "https://github.com/HumanBrainProject/openMINDS/releases/download/v1.0.0/openMINDS_v1.0.0.zip",
                "core": "v1.0.0/core/v3/schema.json",
                "sands": "v1.0.0/SANDS/v1/schemas.json"
            }
        }

        self.download_and_extract()

    def get_version(self, version_name):
        return_version_info = {}
        try:
            return_version_info["core"] = self.cache_dir + "/" + self.versions[version_name]["core"]
            return_version_info["sands"] = self.cache_dir + "/" + self.versions[version_name]["sands"]

            return return_version_info
            
        except Exception as e:
            print(e)
            print("Version not found")
