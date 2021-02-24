import glob
import json
import os
import re
from typing import List

from generator.commons import SchemaStructure, TEMPLATE_PROPERTY_TYPE




def _camel_case_to_human_readable(value:str):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",value).capitalize()

class VocabExtractor(object):

    def __init__(self, schema_information:List[SchemaStructure], root_path):
        self.schema_information = schema_information
        self.root_path = os.path.realpath(root_path)
        self.vocab_path = os.path.join(self.root_path, "vocab")
        self.properties_file = os.path.join(self.vocab_path, "properties.json")
        self.types_file = os.path.join(self.vocab_path, "types.json")

    def _load_properties(self):
        if os.path.exists(self.properties_file):
            with open(self.properties_file, "r") as properties_f:
                self.properties = json.load(properties_f)
            for p in self.properties:
                # We want to make sure that only current (not previously existing) schema definitions are reported. This is why we need to clear the array first
                self.properties[p]["schemas"] = []
                # Same goes for linked types
                self.properties[p]["linkedTypes"] = []
        else:
            self.properties = {}

    def _load_types(self):
        if os.path.exists(self.types_file):
            with open(self.types_file, "r") as types_f:
                self.types = json.load(types_f)
        else:
            self.types = {}

    def _handle_property(self, p, schema, property):
        if p not in self.properties:
            self.properties[p] = {"name": _camel_case_to_human_readable(p), "description": None, "schemas": [], "linkedTypes": []}
        self.properties[p]["schemas"].append(schema)
        self.properties[p]["schemas"] = sorted(set(self.properties[p]["schemas"]))
        self.properties[p]["found"] = True
        if "_linkedTypes" in property:
            for type in property["_linkedTypes"]:
                self.properties[p]["linkedTypes"].append(type)
        self.properties[p]["linkedTypes"] = sorted(set(self.properties[p]["linkedTypes"]))

    def _handle_type(self, type):
        if type not in self.types:
            self.types[type] = {"name": _camel_case_to_human_readable(os.path.basename(type)), "description": None}
        self.types[type]["found"] = True

    def _cleanup_properties(self):
        for p in self.properties:
            if "linkedTypes" in self.properties[p] and self.properties[p]["linkedTypes"] == []:
                del self.properties[p]["linkedTypes"]
            if "found" in self.properties[p] and self.properties[p]["found"]:
                del self.properties[p]["found"]
            else:
                self.properties[p]["deprecated"] = True

    def _cleanup_types(self):
        for t in self.types:
            if "found" in self.types[t] and self.types[t]["found"]:
                del self.types[t]["found"]
            else:
                self.types[t]["deprecated"] = True

    def extract(self):
        self._load_types()
        self._load_properties()
        for schema_info in self.schema_information:
            with open(schema_info.absolute_path, "r") as schema_file:
                schema = json.load(schema_file)
            type = schema[TEMPLATE_PROPERTY_TYPE]
            self._handle_type(type)
            if "properties" in schema:
                for p in schema["properties"]:
                    self._handle_property(p, schema_info.get_relative_path_for_expanded(), schema["properties"][p])
        self._cleanup_types()
        self._cleanup_properties()
        with open(self.types_file, "w") as types_f:
            types_f.write(json.dumps(self.types, sort_keys=True, indent=4))
        with open(self.properties_file, "w") as properties_f:
            properties_f.write(json.dumps(self.properties, sort_keys=True, indent=4))
        return self.types_file, self.properties_file
