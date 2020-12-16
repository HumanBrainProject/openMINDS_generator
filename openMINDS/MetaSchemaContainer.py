import os
from openMINDS.schema_discovery import Schema_Discovery

class MetaSchemaContainer:
    def __init__(self):
        working_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        core_folder = working_dir + "/target/core/v3/schema.json/"
        sands_folder = working_dir + "/target/SANDS/v1/schema.json/"
        self._core = Schema_Discovery(core_folder, "core")
        self._SANDS = Schema_Discovery(sands_folder, "SANDS")
