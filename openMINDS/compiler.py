import os
import openMINDS.MetaSchemaContainer
import openMINDS.version_manager

from openMINDS.schema_discovery import Schema_Discovery


class Helper:
    '''
    Helper class for openMINDS schemas

    This class offers easy discoverability for the schemas of openMINDS core
    and SANDS.
    '''

    def __init__(self, version="v1.0.0"):
        '''
        Generate the objects that allow schema discovery.

        At the moment we only support the current versions of the schemas.
        '''

        # Get the version information from local cache
        version_information = openMINDS.version_manager.Version_Manager().get_version(version)

        # Set up the folder for schema discovery
        working_dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        core_folder = version_information["core"]
        sands_folder = version_information["sands"]

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
            signature, func = openMINDS.MetaSchemaContainer.build_generator(self.core.schemas[schema])
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaContainer.build_help(self.core.schemas[schema])
            class_dictionary[signature] = func

        return type("MetaSchemaContainer", (object,), class_dictionary)(self.core, self.SANDS)
