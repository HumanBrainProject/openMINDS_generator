import json
import copy

import jsonschema
from jsonschema import FormatChecker, ValidationError

from generator.generate_json_schema import JsonSchemaGenerator
from unittest import TestCase

class TestGenerator(TestCase):

    generator = JsonSchemaGenerator("test")
    schema_skeleton = {
        "_type": "https://openminds.ebrains.eu/Test",
        "required": [],
        "properties": {
        }
    }

    def test_embedded_types(self):
        schema = copy.deepcopy(self.schema_skeleton)
        schema["required"].append("propertyWithFormat")
        schema["properties"]["embedded"] = {
            "_embeddedTypes": "https://openminds.ebrains.eu/core/Organization"
        }
        preprocessed = self.generator._pre_process_template(schema)
        processed = self.generator._process_template(preprocessed)
        print(json.dumps(processed, indent=4))
        

    def test_single_format(self):
        schema = copy.deepcopy(self.schema_skeleton)
        schema["required"].append("propertyWithFormat")
        schema["properties"]["propertyWithFormat"] = {
            "type": "string",
            "_format": ["email"]
        }
        preprocessed = self.generator._pre_process_template(schema)
        processed = self.generator._process_template(preprocessed)
        print(json.dumps(processed, indent=4))
        self.assertEqual(processed["properties"]["propertyWithFormat"]["format"], "email")

        valid = {
            "@type": "https://openminds.ebrains.eu/Test",
            "@id": "foobar",
            "propertyWithFormat": "test@test.com"
        }
        jsonschema.validate(valid, processed, format_checker=FormatChecker())

        invalid = {
            "@type": "https://openminds.ebrains.eu/Test",
            "@id": "foobar",
            "propertyWithFormat": "foobar"
        }

        try:
            jsonschema.validate(invalid, processed, format_checker=FormatChecker())
            self.fail("Expected a validation error for invalid payload")
        except ValidationError:
            pass

    def test_multi_format(self):
        schema = copy.deepcopy(self.schema_skeleton)
        schema["required"].append("propertyWithFormat")
        schema["properties"]["propertyWithFormat"] = {
            "type": "string",
            "_format": ["email", "date"]
        }
        preprocessed = self.generator._pre_process_template(schema)
        processed = self.generator._process_template(preprocessed)
        print(json.dumps(processed, indent=4))
        self.assertEqual(processed["properties"]["propertyWithFormat"]["anyOf"], [{"format": "email"}, {"format": "date"}])

        valid1 = {
            "@type": "https://openminds.ebrains.eu/Test",
            "@id": "foobar",
            "propertyWithFormat": "2018-11-13"
        }

        jsonschema.validate(valid1, processed, format_checker=FormatChecker())

        valid2 = {
            "@type": "https://openminds.ebrains.eu/Test",
            "@id": "foobar",
            "propertyWithFormat": "test@test.com"
        }

        jsonschema.validate(valid2, processed, format_checker=FormatChecker())

        invalid = {
            "@type": "https://openminds.ebrains.eu/Test",
            "@id": "foobar",
            "propertyWithFormat": "foobar"
        }

        try:
            jsonschema.validate(invalid, processed, format_checker=FormatChecker())
            self.fail("Expected a validation error for invalid payload")
        except ValidationError:
            pass