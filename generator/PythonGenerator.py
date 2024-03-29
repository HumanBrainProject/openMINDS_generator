"""
Generates openMINDS classes.

"""

import glob
import json
import os
import re
from typing import List
from collections import defaultdict
import warnings

from generator.commons import (
    JinjaGenerator,
    TEMPLATE_PROPERTY_TYPE,
    TEMPLATE_PROPERTY_LINKED_TYPES,
    SchemaStructure,
    TEMPLATE_PROPERTY_EMBEDDED_TYPES,
    SCHEMA_FILE_ENDING,
    ROOT_PATH,
    EXPANDED_DIR,
    find_resource_directories)

LIST_CLASSES_TEMPATE = '''

def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
           if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__.startswith(__name__)]
'''

# in general we make attribute names plural when the attribute can contain multiple items
# the following dict contains exceptions to the simple rule we use for making names plural
# (i.e. add 's' unless the word already ends in 's')
custom_multiple = {
    "data": "data",
    "input_data": "input_data",
    "output_data": "output_data",
    "reference_data": "reference_data",
    "funding": "funding",
    "biological_sex": "biological_sex",
    "age_category": "age_categories",
    "descended_from": "descended_from",
    "laterality": "laterality",
    "software": "software",
    "configuration": "configuration",
    "is_part_of": "is_part_of",
    "semantically_anchored_to": "semantically_anchored_to",
    "is_alternative_version_of": "is_alternative_version_of",
    "experimental_approach": "experimental_approaches",
    "pathology": "pathologies",
    "uncertainty": "uncertainties",
    "application_category": "application_categories",
    "about": "about"
}


def generate_python_name(json_name, allow_multiple=False):
    python_name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", json_name)
    python_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", python_name).lower()

    return python_name

type_name_map = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "array": "list"
}

format_map = {
    "iri": "IRI",
    "date": "date",
    "date-time": "datetime",
    "time": "datetime",
    "email": "str",  # could maybe use Pydantic or something to be stricter about this
    "ECMA262": "str"
}


def generate_class_name(iri):
    parts = iri.split("/")[-2:]
    for i in range(len(parts) - 1):
        parts[i] = parts[i].lower()
    return "openminds." + ".".join(parts)


def generate_doc(property, obj_title):
    if obj_title.upper() == obj_title:  # for acronyms, e.g. DOI
        obj_title_readable = obj_title
    else:
        obj_title_readable = re.sub("([A-Z])", " \g<0>", obj_title).strip().lower()
    doc = property.get("description", "no description available")
    doc = doc.replace("someone or something", f"the {obj_title_readable}")
    doc = doc.replace("something or somebody", f"the {obj_title_readable}")
    doc = doc.replace("something or someone", f"the {obj_title_readable}")
    doc = doc.replace("a being or thing", f"the {obj_title_readable}")
    return doc

def property_name_sort_key(arg):
    """Sort the name field to be first"""
    name, property = arg
    priorities = {
        "name": "0",
        "fullName": "1",
        "shortName": "2",
        "lookupLabel": "3",
    }
    return priorities.get(name, name)


class PythonGenerator(JinjaGenerator):

    def __init__(self, schema_information: List[SchemaStructure]):
        print(os.getcwd())
        super().__init__("py", None, "openMINDS_module_template.py.txt")
        self.target_path = os.path.join("target", "python", "openminds")
        self.schema_information = schema_information
        self.schema_information_by_type = {}
        #self.schema_collection_by_group = {}
        for s in self.schema_information:
            self.schema_information_by_type[s.type] = s
        self.import_data = defaultdict(dict)

    def _pre_process_template(self, schema):
        print("Pre Process template")
        schema_information = self.schema_information_by_type[schema[TEMPLATE_PROPERTY_TYPE]]
        schema["simpleTypeName"] = os.path.basename(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaGroup"] = schema_information.schema_group.split("/")[0]
        schema["schemaVersion"] = schema_information.version
        # if schema["schemaGroup"] not in self.schema_collection_by_group:
        #     self.schema_collection_by_group[schema["schemaGroup"]] = []
        # self.schema_collection_by_group[schema["schemaGroup"]].append(schema_information)

        fields = []
        for name, property in sorted(schema["properties"].items(), key=property_name_sort_key):
            allow_multiple = False
            if property.get("type") == "array":
                allow_multiple = True
            if TEMPLATE_PROPERTY_LINKED_TYPES in property:
                possible_types = [
                    f'"{generate_class_name(iri)}"'
                    for iri in property[TEMPLATE_PROPERTY_LINKED_TYPES]
                ]
            elif TEMPLATE_PROPERTY_EMBEDDED_TYPES in property:
                possible_types = [
                    f'"{generate_class_name(iri)}"'
                    for iri in property[TEMPLATE_PROPERTY_EMBEDDED_TYPES]
                ]  # todo: handle minItems maxItems, e.g. for axesOrigin
            elif "_formats" in property:
                assert property["type"] == "string"
                possible_types = sorted(set([format_map[item] for item in property["_formats"]]))
            elif property.get("type") == "array":
                possible_types = [type_name_map[property["items"]["type"]]]
            else:
                possible_types = [type_name_map[property["type"]]]
            if len(possible_types) == 1:
                possible_types_str = possible_types[0]
            else:
                possible_types_str = "[{}]".format(", ".join(sorted(possible_types)))
            field = {
                "name": generate_python_name(name, allow_multiple),
                "type": possible_types_str,
                "iri": f"vocab:{name}",
                "allow_multiple": allow_multiple,
                "required": name in schema.get("required", []),
                "doc": generate_doc(property, schema["simpleTypeName"])
            }
            fields.append(field)

        # if a given type is found both linked and embedded we use KGObject
        if schema["_type"] in self._embedded_types and not schema["_type"] in self._linked_types:
            base_class = "EmbeddedMetadata"
            default_space = None
        else:
            base_class = "OpenMINDS_Base"
        context = {
            "class_name": generate_class_name(schema[TEMPLATE_PROPERTY_TYPE]).split(".")[-1],
            "base_class": base_class,
            "openminds_type": schema[TEMPLATE_PROPERTY_TYPE],
            "docstring": schema.get("description", ""),
            "fields": fields
        }
        schema.update(context)
        self.import_data[schema["schemaGroup"]][schema[TEMPLATE_PROPERTY_TYPE]] = {
            "class_name": context["class_name"]
        }
        return schema

    def _process_template(self, schema) -> str:
        print("Process template")
        result = super()._process_template(schema)
        return strip_trailing_whitespace(result)

    def _generate_target_file_path(self, schema_group, schema_group_path, schema_path):
        relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
        relative_schema_path = relative_schema_path.replace("-", "_")
        schema_file_name = os.path.basename(schema_path)
        schema_file_name_without_extension = generate_python_name(
            schema_file_name[:-len(SCHEMA_FILE_ENDING)])
        schema_group = schema_group.split("/")[0].lower()
        target_path = os.path.join(
            self.target_path,
            schema_group,
            relative_schema_path,
            f"{schema_file_name_without_extension}.{self.format}")
        return target_path

    def _generate_additional_files(self, schema_group, schema_group_path, schema_path, schema):
        relative_schema_path = os.path.dirname(schema_path[len(schema_group_path) + 1:])
        relative_schema_path = relative_schema_path.replace("-", "_")
        schema_group = schema_group.split("/")[0]
        path_parts = (self.target_path, schema_group.lower(), *relative_schema_path.split("/"))
        # create directories
        os.makedirs(os.path.join(*path_parts), exist_ok=True)
        # write __init__.py files
        schema_file_name = os.path.basename(schema_path)
        path = relative_schema_path.replace(
            "/", ".") + f".{generate_python_name(schema_file_name[:-len(SCHEMA_FILE_ENDING)])}"
        if path[0] != ".":
            path = "." + path
        self.import_data[schema_group][schema[TEMPLATE_PROPERTY_TYPE]]["path"] = path

        for i in range(len(path_parts) + 1):
            path = os.path.join(*path_parts[:i], "__init__.py")
            if not os.path.exists(path):
                with open(path, "w") as fp:
                    fp.write("")

    def _pre_generate(self, ignore=None):
        print("Pre generate")
        self._linked_types = set()
        self._embedded_types = set()
        expanded_path = os.path.join(ROOT_PATH, EXPANDED_DIR)
        for schema_group in find_resource_directories(expanded_path,
                                                      file_ending=SCHEMA_FILE_ENDING,
                                                      ignore=ignore):
            schema_group_path = os.path.join(expanded_path, schema_group)
            for schema_path in glob.glob(os.path.join(schema_group_path,
                                                      f'**/*{SCHEMA_FILE_ENDING}'),
                                         recursive=True):
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)
                for property in schema["properties"].values():
                    if TEMPLATE_PROPERTY_EMBEDDED_TYPES in property:
                        self._embedded_types.update(property[TEMPLATE_PROPERTY_EMBEDDED_TYPES])
                    elif TEMPLATE_PROPERTY_LINKED_TYPES in property:
                        self._linked_types.update(property[TEMPLATE_PROPERTY_LINKED_TYPES])
        if len(self._linked_types.intersection(self._embedded_types)) > 0:
            warnings.warn("Found type(s) that are both embedded and linked")

    def generate(self, ignore=None):
        super().generate(ignore=ignore)
        for schema_group, group_contents in self.import_data.items():
            path = os.path.join(self.target_path, schema_group.lower(), "__init__.py")
            with open(path, "w") as fp:
                fp.write("import sys\nimport inspect\nfrom ...base_v3 import KGObject\n\n")
                for module in group_contents.values():
                    fp.write(f"from {module['path']} import {module['class_name']}\n")
                fp.write(LIST_CLASSES_TEMPATE)
        path = os.path.join(self.target_path, "__init__.py")
        with open(path, "w") as fp:
            module_names = sorted(key.lower() for key in self.import_data)
            fp.write("from . import {}\n".format(", ".join(module_names)))


def strip_trailing_whitespace(s):
    return "\n".join([line.rstrip() for line in s.splitlines()])


if __name__ == "__main__":
    PythonGenerator([]).generate()
