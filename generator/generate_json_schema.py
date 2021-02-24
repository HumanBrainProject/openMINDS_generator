import json
import copy
import os
from typing import List

from generator.commons import TEMPLATE_PROPERTY_TYPE, type_to_schema_url, \
    TEMPLATE_PROPERTY_LINKED_TYPES, Generator, TEMPLATE_PROPERTY_FORMATS, SchemaStructure, TEMPLATE_PROPERTY_EMBEDDED_TYPES
from generator.expander import Expander


class JsonSchemaGenerator(Generator):

    def __init__(self, schema_information:List[SchemaStructure]):
        super().__init__("schema.json")
        self.schema_information = schema_information
        self.schema_information_by_type = {}
        for schema in self.schema_information:
            self.schema_information_by_type[schema.type] = schema
        self.resolved_embedded_schemas = {}

    def _handle_property(self, property):
        self._resolve_jsonschema_templates(property)
        self._handle_formats(property)

    def _handle_formats(self, property):
        if TEMPLATE_PROPERTY_FORMATS in property:
            formats = property[TEMPLATE_PROPERTY_FORMATS]
            if len(formats) == 1:
                property["format"] = formats[0]
            elif len(formats)>0:
                property["anyOf"] = [{"format": f} for f in formats]
            del property[TEMPLATE_PROPERTY_FORMATS]

    @staticmethod
    def _set_type_if_it_doesnt_exist(property):
        if "type" not in property:
            # Make sure, that a type is defined - let's default to object
            property["type"] = "object"
        target = property
        if property["type"] == "array":
            target = {}
            property["items"] = target
        return target

    def _prepare_embedded_schema(self, embedded_schema):
        embedded_schema["type"] = "object"
        return embedded_schema

    def _handle_embedded_links(self, schema):
        for p in schema["properties"]:
            if TEMPLATE_PROPERTY_EMBEDDED_TYPES in schema["properties"][p]:
                embedded_schemas = []
                for t in schema["properties"][p][TEMPLATE_PROPERTY_EMBEDDED_TYPES]:
                    if t in self.resolved_embedded_schemas:
                        embedded_schemas.append(self.resolved_embedded_schemas[t])
                    else:
                        if t in self.schema_information_by_type:
                            schema_info_of_embedded_type = self.schema_information_by_type[t]
                            with open(os.path.join(Expander.get_absolute_expanded_dir(), schema_info_of_embedded_type.get_relative_path_for_expanded()),
                                      "r") as embedded_schema_file:
                                embedded_schema = json.load(embedded_schema_file)
                            handled_schema = self._handle_embedded_links(embedded_schema)
                            prepared_schema = self._prepare_embedded_schema(handled_schema)
                            self.resolved_embedded_schemas[t] = prepared_schema
                            embedded_schemas.append(prepared_schema)
                        else:
                            print(f"Was looking for the embedded type {t} but couldn't find a schema")
                if len(embedded_schemas)>1:
                    schema["properties"][p] = {"anyOf": embedded_schemas}
                elif len(embedded_schemas)==1:
                    schema["properties"][p] = embedded_schemas[0]
        return schema

    def _resolve_jsonschema_templates(self, property):
        if TEMPLATE_PROPERTY_LINKED_TYPES in property:
            target = JsonSchemaGenerator._set_type_if_it_doesnt_exist(property)
            target["if"] = {"required": ["@type"]}
            target["then"] = {
                "properties": {
                    "@id": {
                        "type": "string",
                        "format": "iri"
                    },
                    "@type": {
                        "type": "string",
                        "format": "iri",
                        "enum": property[TEMPLATE_PROPERTY_LINKED_TYPES]
                    }},
                "required": ["@id"]
            }
            target["else"] = {
                "properties": {
                    "@id": {
                        "type": "string",
                        "format": "iri"
                    }
                },
                "required": ["@id"]
            }
            del property[TEMPLATE_PROPERTY_LINKED_TYPES]

    @staticmethod
    def _clear_template_properties(schema):
        if TEMPLATE_PROPERTY_TYPE in schema:
            del schema[TEMPLATE_PROPERTY_TYPE]

    def _process_template(self, schema) -> str:
        schema = copy.deepcopy(schema)
        schema["$schema"] = "http://json-schema.org/draft-07/schema#"

        required = schema["required"] if "required" in schema else []
        required.append("@id")
        required.append("@type")
        schema["required"] = list(set(required))

        if "properties" not in schema:
            schema["properties"] = {}

        properties = schema["properties"]
        properties["@id"] = {
            "type": "string",
            "description": "Metadata node identifier."
        }

        if TEMPLATE_PROPERTY_TYPE in schema:
            schema_id = type_to_schema_url(schema[TEMPLATE_PROPERTY_TYPE])
            schema["$id"] = schema_id
            schema["type"] = "object"
            properties["@type"] = {"type": "string", "const": schema[TEMPLATE_PROPERTY_TYPE]}

        for property_key in properties:
            self._handle_property(properties[property_key])

        self._handle_embedded_links(schema)
        return json.dumps(schema, indent=4, sort_keys=True)


if __name__ == "__main__":
    JsonSchemaGenerator([]).generate()
