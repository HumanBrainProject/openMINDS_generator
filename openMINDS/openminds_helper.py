import os

from openMINDS.schema_discovery import Schema_Discovery


class OpenMINDS_helper:
    '''
    Helper class for openMINDS schemas

    This class offers easy discoverability for the schemas of openMINDS core
    and SANDS.
    '''

    def __init__(self):
        '''
        Generate the objects that allow schema discovery.

        At the moment we only support the current versions of the schemas.
        '''

        # Set up the folder for schema discovery
        working_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        core_folder = working_dir + "/target/core/v3/schema.json/"
        sands_folder = working_dir + "/target/SANDS/v1/schema.json/"

        # Discover schemas available in the folders defined above
        self.core = Schema_Discovery(core_folder, "core")
        self.SANDS = Schema_Discovery(sands_folder, "SANDS")
