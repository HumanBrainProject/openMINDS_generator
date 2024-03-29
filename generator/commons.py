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
TEMPLATE_PROPERTY_EMBEDDED_CATEGORIES = "_embeddedCategories"

OPENMINDS_VOCAB="https://openminds.ebrains.eu/vocab/"

EXPANDED_DIR = "expanded"

SCHEMA_FILE_ENDING = ".schema.tpl.json"
INSTANCE_FILE_ENDING = ".jsonld"

ROOT_PATH = os.path.realpath(".")
TARGET_PATH = os.path.join(ROOT_PATH, "target")


class SchemaStructure:

    def __init__(self, type, schema_group, version, file):
        self.type = type
        self.schema_group = schema_group
        self.file = file
        self.version = version
        self.categories = None
        self.absolute_path = None

    def set_categories(self, categories):
        self.categories = categories

    def set_absolute_path(self, absolute_path):
        self.absolute_path = absolute_path

    def get_relative_path_for_expanded(self):
        return f"{self.schema_group}/{self.version}/{self.file}"

    def get_schema_name(self):
        return self.get_relative_path_for_expanded()[0:-len(SCHEMA_FILE_ENDING)]


def find_resource_directories(root_path, file_ending, ignore=None):
    def ignore_dir(path):
        if ignore:
            for ignore_name in ignore:
                if ignore_name in path:
                    return True
        return False

    resource_directories = set()
    for source in glob.glob(os.path.join(root_path, f'**/*{file_ending}'), recursive=True):
        resource_dir = os.path.dirname(source)[len(root_path) + 1:]
        if ("target" not in resource_dir
            and EXPANDED_DIR not in resource_dir
            and not ignore_dir(resource_dir)
        ):
            path_split = resource_dir.split("/")
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
        self._pre_generate(ignore=ignore)
        if os.path.exists(self.target_path):
            print("clearing previously generated files")
            shutil.rmtree(self.target_path)
        os.makedirs(self.target_path, exist_ok=True)
        expanded_path = os.path.join(ROOT_PATH, EXPANDED_DIR)
        for schema_group in find_resource_directories(expanded_path, file_ending=SCHEMA_FILE_ENDING, ignore=ignore):
            print(f"handle {schema_group}")
            schema_group_path = os.path.join(expanded_path, schema_group)
            for schema_path in glob.glob(os.path.join(schema_group_path, f'**/*{SCHEMA_FILE_ENDING}'), recursive=True):
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                self._pre_process_template(schema)

                self._generate_additional_files(schema_group, schema_group_path, schema_path, schema)
                target_file_path = self._generate_target_file_path(schema_group, schema_group_path, schema_path)
                print(f"Rendering {target_file_path}")
                result = self._process_template(schema)
                with open(target_file_path, "w", encoding="utf-8") as target_file:
                    target_file.write(result)
                self.written_files.append(target_file_path)

    def _generate_additional_files(self, schema_group, schema_group_path, schema_path, schema):
        relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
        os.makedirs(os.path.join(self.target_path, schema_group, relative_schema_path), exist_ok=True)

    def _generate_target_file_path(self, schema_group, schema_group_path, schema_path):
        relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
        schema_file_name = os.path.basename(schema_path)
        schema_file_name_without_extension = schema_file_name[:-len(SCHEMA_FILE_ENDING)]
        return os.path.join(self.target_path, schema_group, relative_schema_path,
                            f"{schema_file_name_without_extension}.{self.format}")

    def _process_template(self, schema) -> str:
        return schema

    def _pre_process_template(self, schema):
        return schema

    def _pre_generate(self, ignore=None):
        pass


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
