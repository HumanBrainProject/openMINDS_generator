import os
import git
import urllib3
import tempfile
import pathlib
import zipfile

class Version_Manager:

    def __init__(self):
        home = str(pathlib.Path.home())
        self.cache_dir = home + "/.openMINDS"
        pathlib.Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

        self.versions = {
            "dev": "https://github.com/HumanBrainProject/openMINDS/suites/2113925983/artifacts/43039730",
            "v1.0.0": "https://github.com/HumanBrainProject/openMINDS/releases/download/v1.0.0/openMINDS_v1.0.0.zip"
        }

        http = urllib3.PoolManager()
        response = http.request('GET', self.versions["v1.0.0"])
        datatowrite = response.data

        print("Download start")

        v1_folder = self.cache_dir + "/v1.0.0/"
        pathlib.Path(v1_folder).mkdir(parents=True, exist_ok=True)

        with open(v1_folder + "v1.zip", 'wb+') as f:
            f.write(datatowrite)

        print("Download success")
