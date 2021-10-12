import glob
import json
import os
import shutil
from json.decoder import JSONDecodeError
from typing import List

from generator.commons import TEMPLATE_PROPERTY_EXTENDS, TEMPLATE_PROPERTY_TYPE, find_resource_directories, EXPANDED_DIR, SCHEMA_FILE_ENDING, SchemaStructure, \
    TEMPLATE_PROPERTY_CATEGORIES, TEMPLATE_PROPERTY_LINKED_CATEGORIES, TEMPLATE_PROPERTY_LINKED_TYPES

class Expander(object):

    def __init__(self, path, vocab, ignore=None):
        self.root_path = os.path.realpath(path)
        self.vocab = vocab
        self.get_absolute_expanded_dir = Expander.get_absolute_expanded_dir()
        self.schemas = self._find_schemas(ignore=ignore)
        self._schemas_by_category = None

    @staticmethod
    def get_absolute_expanded_dir():
        return os.path.realpath(os.path.join(os.path.realpath("."), EXPANDED_DIR))

    def enrich_with_vocab(self, types_file, properties_file):
        with open(types_file, "r") as types_file_path:
            types = json.load(types_file_path)
        with open(properties_file, "r") as properties_file_path:
            properties = json.load(properties_file_path)
        for schema_info in self.schemas:
            print(f"Enriching schema {schema_info.file}")
            with open(schema_info.absolute_path, "r") as schema_file:
                schema = json.load(schema_file)
            type = schema[TEMPLATE_PROPERTY_TYPE]
            if type in types:
                t = types[type]
                if "deprecated" in t and t["deprecated"]:
                    schema["_deprecated"] = True
                if "description" in t and t["description"]:
                    schema["description"] = t["description"]
                if "name" in t and t["name"]:
                    schema["title"] = t["name"]
            for p in schema["properties"]:
                qualified_p = f"{self.vocab}{p}"
                if qualified_p in properties:
                    prop = properties[qualified_p]
                    if "description" in prop and prop["description"]:
                        schema["properties"][p]["description"] = prop["description"]
                    if "name" in prop and prop["name"]:
                        schema["properties"][p]["title"] = prop["name"]
                    if "sameAs" in prop and prop["sameAs"]:
                        schema["properties"][p]["_sameAs"] = prop["sameAs"]
            with open(schema_info.absolute_path, "w") as schema_file:
                schema_file.write(json.dumps(schema, indent=4))

    def _process_schema_first_pass(self, source_schema, schema, schema_group):
        if TEMPLATE_PROPERTY_EXTENDS in schema:
            if schema[TEMPLATE_PROPERTY_EXTENDS].startswith("/"):
                extends_split = schema[TEMPLATE_PROPERTY_EXTENDS].split("/")
                extension_schema_group = extends_split[1]
                # For cross-submodule references, we allow the schemas to declare "absolute" paths which need to be relativated against the processing directory in this step.
                extension_path = os.path.realpath(os.path.join(self.root_path, schema[TEMPLATE_PROPERTY_EXTENDS][1:]))
            else:
                extension_schema_group = schema_group
                extension_path = os.path.realpath(os.path.join(self.root_path, schema_group, "schemas", schema[TEMPLATE_PROPERTY_EXTENDS]))
            if extension_path.startswith(self.root_path) and os.path.isfile(extension_path):
                # Only load the extension if it is part of the same schema group (and if it exists)
                # (prevent access of resources outside of the directory structure)
                with open(extension_path, "r") as extension_file:
                    extension = json.load(extension_file)
                # We need to extend the extension itself first to ensure that we can handle multi-level extensions...
                extended_schema = self._process_schema_first_pass(source_schema, extension, extension_schema_group)
                Expander._apply_extension(schema, extended_schema)
            del schema[TEMPLATE_PROPERTY_EXTENDS]
        if TEMPLATE_PROPERTY_CATEGORIES in schema and schema[TEMPLATE_PROPERTY_CATEGORIES]:
            source_schema.set_categories(schema[TEMPLATE_PROPERTY_CATEGORIES])
        return schema

    def expand(self):
        absolute_target_dir = Expander.get_absolute_expanded_dir()
        if os.path.exists(absolute_target_dir):
            print("clearing previously generated expanded sources")
            shutil.rmtree(absolute_target_dir)
        for schema in self.schemas:
            print(f"handling schema for {schema.type} - 1st pass")
            try:
                print(f"handling schema for {schema.type}")
                absolute_schema_group_target_dir = os.path.realpath(os.path.join(absolute_target_dir, schema.schema_group, schema.version))
                absolute_schema_group_src_dir = self.root_path if schema.schema_group == '' else os.path.join(self.root_path, schema.schema_group, "schemas")
                print(f"process {schema.file}")
                with open(os.path.join(absolute_schema_group_src_dir, schema.file), "r") as schema_file:
                    schema_payload = json.load(schema_file)
                schema_target_path = os.path.join(absolute_schema_group_target_dir, schema.file)
                self._process_schema_first_pass(schema, schema_payload, schema.schema_group)
                schema.set_absolute_path(schema_target_path)
                os.makedirs(os.path.dirname(schema_target_path), exist_ok=True)
                with open(schema_target_path, "w") as target_file:
                    target_file.write(json.dumps(schema_payload, indent=4))
            except JSONDecodeError:
                print(f"Skipping schema {schema.file} because it is not a valid JSON document")
        self._schemas_by_category = Expander._schemas_by_category(self.schemas)
        for schema in self.schemas:
            print(f"handling schema for {schema.type} - 2nd pass")
            self._process_schema_second_pass(schema)

    @staticmethod
    def _schemas_by_category(schemas: List[SchemaStructure]) -> dict:
        result = {}
        for s in schemas:
            if s.categories:
                for c in s.categories:
                    if c not in result:
                        result[c] = []
                    result[c].append(s.type)
        return result

    def _find_schemas(self, ignore=None) -> List[SchemaStructure]:
        schema_information = []
        for schema_group in find_resource_directories(self.root_path, file_ending=SCHEMA_FILE_ENDING, ignore=ignore):
            schema_group = schema_group.split("/")[0]
            version_path = os.path.join(self.root_path, schema_group, "version.txt")
            if os.path.isfile(version_path):
                with open(version_path, "r") as version_file:
                    version = version_file.read().strip()
            else:
                version = "v0"
            absolute_schema_group_src_dir = os.path.join(self.root_path, schema_group, "schemas")
            if os.path.isdir(absolute_schema_group_src_dir):
                print(f"handling schemas of {schema_group}")
                for schema_path in glob.glob(os.path.join(self.root_path, schema_group, "schemas", f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
                    relative_schema_path = schema_path[len(absolute_schema_group_src_dir) + 1:]
                    try:
                        with open(schema_path, "r") as schema_file:
                            schema = json.load(schema_file)
                        if TEMPLATE_PROPERTY_TYPE in schema:
                            schema_information.append(
                                SchemaStructure(schema[TEMPLATE_PROPERTY_TYPE], schema_group, version, relative_schema_path))
                        else:
                            print(f"Skipping schema {relative_schema_path} because it doesn't contain a valid type")
                    except JSONDecodeError:
                        print(f"Skipping schema {relative_schema_path} because it is not a valid JSON document")
            else:
                print(f"Skipping schemas of {schema_group} since there is no schemas directory")
        return schema_information

    def _process_schema_second_pass(self, schema):
        with open(schema.absolute_path, "r") as schema_file:
            schema_payload = json.load(schema_file)
        if "properties" in schema_payload:
            for p in schema_payload["properties"]:
                if TEMPLATE_PROPERTY_LINKED_CATEGORIES in schema_payload["properties"][p]:
                    linked_categories = schema_payload["properties"][p][TEMPLATE_PROPERTY_LINKED_CATEGORIES]
                    linked_types = []
                    for linked_category in linked_categories:
                        if linked_category in self._schemas_by_category:
                            linked_types.extend(self._schemas_by_category[linked_category])
                    schema_payload["properties"][p][TEMPLATE_PROPERTY_LINKED_TYPES] = linked_types
                    del schema_payload["properties"][p][TEMPLATE_PROPERTY_LINKED_CATEGORIES]
        with open(schema.absolute_path, "w") as target_file:
            target_file.write(json.dumps(schema_payload, indent=4))

    @staticmethod
    def _apply_extension(source, extension):
            #Required has to be a list...
            if "required" in extension:
                if "required" not in source:
                    source["required"] = extension["required"]
                elif type(source["required"]) is list and type(extension["required"]) is list:
                    source["required"] = list(set(source["required"] + extension["required"]))
            if "properties" not in source:
                source["properties"] = {}

            if TEMPLATE_PROPERTY_CATEGORIES in extension:
                if TEMPLATE_PROPERTY_CATEGORIES not in source:
                    source[TEMPLATE_PROPERTY_CATEGORIES] = extension[TEMPLATE_PROPERTY_CATEGORIES]
                elif type(source[TEMPLATE_PROPERTY_CATEGORIES]) is list and type(extension[TEMPLATE_PROPERTY_CATEGORIES]) is list:
                    source[TEMPLATE_PROPERTY_CATEGORIES] = list(set(source[TEMPLATE_PROPERTY_CATEGORIES] + extension[TEMPLATE_PROPERTY_CATEGORIES]))

            for k in extension["properties"]:
                property_from_extension = extension["properties"][k]
                if k in source["properties"]:
                    property_from_source = source["properties"][k]
                    for property_spec_key in property_from_extension:
                        # Only apply the specification element from the extension if it doesn't yet exist in the source
                        if property_spec_key not in property_from_source:
                            property_from_source[property_spec_key] = property_from_extension[property_spec_key]
                else:
                    #If the property is not in the source yet at all, we add it as a whole from the extension
                    source["properties"][k] = extension["properties"][k]