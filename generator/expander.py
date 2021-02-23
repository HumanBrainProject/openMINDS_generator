import glob
import json
import os
import shutil
from typing import List

from generator.commons import TEMPLATE_PROPERTY_EXTENDS, TEMPLATE_PROPERTY_TYPE, find_resource_directories, EXPANDED_DIR, SCHEMA_FILE_ENDING, SchemaStructure, \
    TEMPLATE_PROPERTY_CATEGORIES, TEMPLATE_PROPERTY_LINKED_CATEGORIES, TEMPLATE_PROPERTY_LINKED_TYPES

DEEP_MERGE_PROPERTIES = ["properties", "required"]


class Expander(object):

    @staticmethod
    def get_absolute_expanded_dir():
        return os.path.realpath(os.path.join(os.path.realpath("."), EXPANDED_DIR))

    @staticmethod
    def expand(path_to_schemas):
        schema_root_path = os.path.realpath(path_to_schemas)
        absolute_target_dir = Expander.get_absolute_expanded_dir()
        if os.path.exists(absolute_target_dir):
            print("clearing previously generated expanded sources")
            shutil.rmtree(absolute_target_dir)
        schemas = Expander._find_schemas(schema_root_path)
        schemas_by_category = Expander._schemas_by_category(schemas)
        for schema in schemas:
            print(f"handling schema for {schema.type}")
            absolute_schema_group_target_dir = os.path.realpath(os.path.join(absolute_target_dir, schema.schema_group, schema.version))
            absolute_schema_group_src_dir = schema_root_path if schema.schema_group == '' else os.path.join(schema_root_path, schema.schema_group)
            print(f"process {schema.file}")
            with open(os.path.join(absolute_schema_group_src_dir, schema.file), "r") as schema_file:
                schema_payload = json.load(schema_file)
            schema_target_path = os.path.join(absolute_schema_group_target_dir, schema.file)
            Expander._process_schema(schema_payload, schema.schema_group, schema_root_path, schemas_by_category)
            os.makedirs(os.path.dirname(schema_target_path), exist_ok=True)
            with open(schema_target_path, "w") as target_file:
                target_file.write(json.dumps(schema_payload, indent=4))
        return schemas

    @staticmethod
    def _schemas_by_category(schemas:List[SchemaStructure]) -> dict:
        result = {}
        for s in schemas:
            if s.categories:
                for c in s.categories:
                    if c not in result:
                        result[c] = []
                    result[c].append(s.type)
        return result

    @staticmethod
    def _find_schemas(schema_root_path) -> List[SchemaStructure]:
        schema_information = []
        for schema_group in find_resource_directories(schema_root_path):
            group_name = schema_group.split("/")[0]
            with open(os.path.join(schema_root_path, group_name, "version.txt"), "r") as version_file:
                version = version_file.read().strip()
            absolute_schema_group_src_dir = os.path.join(schema_root_path, schema_group)
            print(f"handling schemas of {schema_group}")
            for schema_path in glob.glob(os.path.join(schema_root_path, schema_group, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
                relative_schema_path = schema_path[len(absolute_schema_group_src_dir) + 1:]
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                if TEMPLATE_PROPERTY_TYPE in schema:
                    schema_information.append(SchemaStructure(schema[TEMPLATE_PROPERTY_TYPE], schema[TEMPLATE_PROPERTY_CATEGORIES] if TEMPLATE_PROPERTY_CATEGORIES in schema else None, schema_group, version, relative_schema_path))
                else:
                    print(f"Skipping schema {relative_schema_path} because it doesn't contain a valid type")
        return schema_information


    @staticmethod
    def _process_schema(schema, schema_group, schema_root_path, schemas_by_category):
        if TEMPLATE_PROPERTY_EXTENDS in schema:
            extension_path = os.path.realpath(os.path.join(schema_root_path, schema_group, schema[TEMPLATE_PROPERTY_EXTENDS]))
            if extension_path.startswith(schema_root_path):
                # Only load the extension if it is part of the same schema group
                # (prevent access of resources outside of the directory structure)
                with open(extension_path, "r") as extension_file:
                    extension = json.load(extension_file)
                Expander._apply_extension(schema, extension)
            del schema[TEMPLATE_PROPERTY_EXTENDS]
        if "properties" in schema:
            for p in schema["properties"]:
                if TEMPLATE_PROPERTY_LINKED_CATEGORIES in schema["properties"][p]:
                    linked_categories = schema["properties"][p][TEMPLATE_PROPERTY_LINKED_CATEGORIES]
                    linked_types = []
                    for linked_category in linked_categories:
                        if linked_category in schemas_by_category:
                            linked_types.extend(schemas_by_category[linked_category])
                    schema["properties"][p][TEMPLATE_PROPERTY_LINKED_TYPES] = linked_types
                    del schema["properties"][p][TEMPLATE_PROPERTY_LINKED_CATEGORIES]
        return schema

    @staticmethod
    def _apply_extension(source, extension):
        for extension_key in extension:
            if extension_key in DEEP_MERGE_PROPERTIES and extension_key in source:
                if type(source[extension_key]) is list and type(extension[extension_key]) is list:
                    source[extension_key] = source[extension_key]+extension[extension_key]
                elif type(source[extension_key]) is dict and type(extension[extension_key]) is dict:
                    for property_key in extension[extension_key]:
                        if property_key not in source[extension_key]:
                            source[extension_key][property_key] = extension[extension_key][property_key]
            if extension_key not in source:
                source[extension_key] = extension[extension_key]


if __name__ == "__main__":
    Expander().expand()
