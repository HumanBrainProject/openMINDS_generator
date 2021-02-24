import os
import git
import tempfile
from pathlib import Path

class Version_Manager:

    def __init__(self):
        home = str(Path.home())
        self.cache_dir = home + "/.openMINDS"
