import os
import json
import openMINDS.MetaSchemaCollection

from pathlib import Path
from openMINDS.schema_discovery import Schema_Discovery

class Helper:
    '''
    Helper class for openMINDS schemas

    This class offers easy discoverability for the schemas of openMINDS core
    and SANDS.
    '''

    def __init__(self):
        '''
        Generate the objects that allow schema discovery.
        '''
        with open(os.path.join(Path.home(), ".openMINDS.conf"), "r") as f:
            config = json.load(f)
        
            # Get the version information from local cache
            #version_information = openMINDS.version_manager.Version_Manager().get_version(config["selected_version"])

            # Discover schemas available in the folders defined above
            self.core = Schema_Discovery(os.path.join(config["openMINDS_directory"] + "/" + config["selected_version"] + "/core"), "core")
            self.SANDS = Schema_Discovery(os.path.join(config["openMINDS_directory"] + "/" + config["selected_version"] + "/SANDS"), "SANDS")
            self.controlledTerms = Schema_Discovery(os.path.join(config["openMINDS_directory"] + "/" + config["selected_version"] + "/controlledTerms"), "controlledTerms")


    def create_collection(self):
        class_dictionary = {}
        class_dictionary["__init__"] = openMINDS.MetaSchemaCollection.build_constructor()
        class_dictionary["save"] = openMINDS.MetaSchemaCollection.build_save()
        class_dictionary["get"] = openMINDS.MetaSchemaCollection.build_get()

        for schema in self.core.schemas:
            signature, func = openMINDS.MetaSchemaCollection.build_adder(self.core.schemas[schema])
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_generator(self.core.schemas[schema])
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_help(self.core.schemas[schema])
            class_dictionary[signature] = func

        for schema in self.SANDS.schemas:
            signature, func = openMINDS.MetaSchemaCollection.build_adder(self.SANDS.schemas[schema])
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_generator(self.SANDS.schemas[schema], substructure=False)
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_help(self.SANDS.schemas[schema], substructure=False)
            class_dictionary[signature] = func

        for schema in self.controlledTerms.schemas:
            signature, func = openMINDS.MetaSchemaCollection.build_adder(self.controlledTerms.schemas[schema])
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_generator(self.controlledTerms.schemas[schema], substructure=False)
            class_dictionary[signature] = func
            signature, func = openMINDS.MetaSchemaCollection.build_help(self.controlledTerms.schemas[schema], substructure=False)
            class_dictionary[signature] = func

        return type("MetaSchemaCollection", (object,), class_dictionary)(self.core, self.SANDS)
