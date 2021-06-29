import json
import os
import re
from typing import List

from generator.commons import SchemaStructure, TEMPLATE_PROPERTY_TYPE, OPENMINDS_VOCAB


def _camel_case_to_human_readable(value:str):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",value).capitalize()

class VocabExtractor(object):

    def __init__(self, schema_information:List[SchemaStructure], root_path, reinit):
        self.schema_information = schema_information
        self.root_path = os.path.realpath(root_path)
        self.vocab_path = os.path.join(self.root_path, "vocab")
        self.properties_file = os.path.join(self.vocab_path, "properties.json")
        self.types_file = os.path.join(self.vocab_path, "types.json")
        self.reinit = reinit

    def _load_properties(self):
        if os.path.exists(self.properties_file):
            with open(self.properties_file, "r") as properties_f:
                self.properties = json.load(properties_f)
            if self.reinit:
                for p in self.properties:
                    # We want to make sure that only current (not previously existing) schema definitions are reported. This is why we need to clear the array first
                    self.properties[p]["schemas"] = []
        else:
            self.properties = {}

    def _load_types(self):
        if os.path.exists(self.types_file):
            with open(self.types_file, "r") as types_f:
                self.types = json.load(types_f)
            if self.reinit:
                for t in self.types:
                    self.types[t]["schemas"] = []
        else:
            self.types = {}

    def _handle_property(self, p, schema):
        qualified_p = f"{OPENMINDS_VOCAB}{p}"
        if qualified_p not in self.properties:
            self.properties[qualified_p] = {"label": _camel_case_to_human_readable(p), "description": None, "schemas": [], "linkedTypes": [], "sameAs": []}
        self.properties[qualified_p]["name"] = p
        if "schemas" not in self.properties[qualified_p] or not self.properties[qualified_p]["schemas"]:
            self.properties[qualified_p]["schemas"] = []
        self.properties[qualified_p]["schemas"].append(schema)
        self.properties[qualified_p]["schemas"] = sorted(set(self.properties[qualified_p]["schemas"]))

    def _handle_type(self, type, schema):
        if type not in self.types:
            self.types[type] = {"name": _camel_case_to_human_readable(os.path.basename(type)), "description": None, "translatableTo": None, "schemas": []}
        if "schemas" not in self.types[type] or not self.types[type]["schemas"]:
            self.types[type]["schemas"] = []
        self.types[type]["schemas"].append(schema)
        self.types[type]["schemas"] = sorted(set(self.types[type]["schemas"]))

    def extract(self):
        self._load_types()
        self._load_properties()
        for schema_info in self.schema_information:
            with open(schema_info.absolute_path, "r") as schema_file:
                schema = json.load(schema_file)
            type = schema[TEMPLATE_PROPERTY_TYPE]
            self._handle_type(type, schema_info.get_schema_name())
            if "properties" in schema:
                for p in schema["properties"]:
                    self._handle_property(p, schema_info.get_schema_name())
        with open(self.types_file, "w") as types_f:
            types_f.write(json.dumps(self.types, sort_keys=True, indent=4))
        with open(self.properties_file, "w") as properties_f:
            properties_f.write(json.dumps(self.properties, sort_keys=True, indent=4))
        return self.types_file, self.properties_file
