import os
import openMINDS.MetaSchemaContainer

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


    def get_container(self):
        class_dictionary = {}
        class_dictionary["__init__"] = openMINDS.MetaSchemaContainer.build_constructor()
        class_dictionary["save"] = openMINDS.MetaSchemaContainer.build_save()
        class_dictionary["get"] = openMINDS.MetaSchemaContainer.build_get()

        for schema in self.core.schemas:
            signature, func = openMINDS.MetaSchemaContainer.build_adder(self.core.schemas[schema])
            class_dictionary[signature] = func

        return type("MetaSchemaContainer", (object,), class_dictionary)(self.core, self.SANDS)
