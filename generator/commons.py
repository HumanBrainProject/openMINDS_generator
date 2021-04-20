import glob
import os
import json
import shutil

from jinja2 import Environment, select_autoescape, FileSystemLoader

TEMPLATE_PROPERTY_TYPE = "_type"
TEMPLATE_PROPERTY_EXTENDS = "_extends"
TEMPLATE_PROPERTY_LINKED_TYPES = "_linkedTypes"
TEMPLATE_PROPERTY_EMBEDDED_TYPES = "_embeddedTypes"
TEMPLATE_PROPERTY_FORMATS = "_formats"
TEMPLATE_PROPERTY_CATEGORIES = "_categories"
TEMPLATE_PROPERTY_LINKED_CATEGORIES = "_linkedCategories"


EXPANDED_DIR = "expanded"

SCHEMA_FILE_ENDING = ".schema.tpl.json"

ROOT_PATH = os.path.realpath(".")
TARGET_PATH = os.path.join(ROOT_PATH, "target")


class SchemaStructure:

    def __init__(self, type, categories, schema_group, version, file):
        self.type = type
        self.categories = categories
        self.schema_group = schema_group
        self.file = file
        self.version = version

    def set_absolute_path(self, absolute_path):
        self.absolute_path = absolute_path

    def get_relative_path_for_expanded(self):
        return f"{self.schema_group}/{self.version}/{self.file}"


def find_resource_directories(schema_root_path, ignore=None):
    def ignore_dir(path):
        if ignore:
            for ignore_name in ignore:
                if ignore_name in path:
                    return True
        return False

    resource_directories = set()
    for schema_source in glob.glob(os.path.join(schema_root_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
        schema_resource_dir = os.path.dirname(schema_source)[len(schema_root_path)+1:]
        if ("target" not in schema_resource_dir
            and EXPANDED_DIR not in schema_resource_dir
            and not ignore_dir(schema_resource_dir)
        ):
            path_split = schema_resource_dir.split("/")
            if len(path_split) == 1:
                resource_directories.add(path_split[0])
            else:
                resource_directories.add("/".join([path_split[0], path_split[1]]))
    return list(resource_directories)


def type_to_schema_url(t):
    type_base = os.path.dirname(t)
    type_name = os.path.basename(t)
    schema_name = type_name[0].lower()+type_name[1:]
    return f"{type_base}/{schema_name}?format=json-schema"


def type_to_html_url(t):
    type_base = os.path.dirname(t)
    type_name = os.path.basename(t)
    schema_name = type_name[0].lower()+type_name[1:]
    return f"{type_base}/{schema_name}?format=html"

def _get_properties_with_unresolved_embedded_types(payload):
    embedded_types = []
    if "properties" in payload:
        for p in payload["properties"]:
            if TEMPLATE_PROPERTY_EMBEDDED_TYPES in payload["properties"][p]:
                embedded_types.append(p)
    return embedded_types



class Generator(object):

    def __init__(self, format):
        self.format = format
        self.target_path = os.path.join(TARGET_PATH, self.format)
        self.written_files = []

    def generate(self, ignore=None):
        if os.path.exists(self.target_path):
            print("clearing previously generated files")
            shutil.rmtree(self.target_path)
        expanded_path = os.path.join(ROOT_PATH, EXPANDED_DIR)
        for schema_group in find_resource_directories(expanded_path, ignore=ignore):
            print(f"handle {schema_group}")
            schema_group_path = os.path.join(expanded_path, schema_group)
            for schema_path in glob.glob(os.path.join(schema_group_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
                relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
                schema_file_name = os.path.basename(schema_path)
                schema_file_name_without_extension = schema_file_name[:-len(SCHEMA_FILE_ENDING)]
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                self._pre_process_template(schema)
                os.makedirs(os.path.join(self.target_path, schema_group, relative_schema_path), exist_ok=True)
                target_file_path = os.path.join(self.target_path, schema_group, relative_schema_path,
                                                f"{schema_file_name_without_extension}.{self.format}")
                print(f"Rendering {target_file_path}")
                result = self._process_template(schema)
                with open(target_file_path, "w", encoding="utf-8") as target_file:
                    target_file.write(result)
                self.written_files.append(target_file_path)

    def _process_template(self, schema) -> str:
        return schema

    def _pre_process_template(self, schema):
        return schema


class JinjaGenerator(Generator):

    def __init__(self, format, autoescape, template_name):
        super().__init__(format)
        self.template_name = template_name
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
            autoescape=select_autoescape(autoescape) if autoescape is not None else select_autoescape()
        )

    def _process_template(self, schema) -> str:
        return self.env.get_template(self.template_name).render(schema)

    def _pre_process_template(self, schema):
        pass
