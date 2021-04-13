import os
from typing import List

from generator.commons import JinjaGenerator, TEMPLATE_PROPERTY_TYPE, \
    type_to_schema_url, TEMPLATE_PROPERTY_LINKED_TYPES, type_to_html_url, SchemaStructure, TEMPLATE_PROPERTY_EMBEDDED_TYPES


class PlantUMLGenerator(JinjaGenerator):

    def __init__(self, schema_information: List[SchemaStructure]):
        super().__init__("uml", [], "uml_template.puml")
        self.schema_information = schema_information
        self.schema_information_by_type = {}
        for s in self.schema_information:
            self.schema_information_by_type[s.type] = s

    def _pre_process_template(self, schema):
        schema_information = self.schema_information_by_type[schema[TEMPLATE_PROPERTY_TYPE]]
        schema["simpleTypeName"] = os.path.basename(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaId"] = type_to_schema_url(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaGroup"] = schema_information.schema_group.split("/")[0]
        schema["schemaVersion"] = schema_information.version
        for property, propertyValue in schema["properties"].items():
            propertyValue["typeInformation"] = []
            if TEMPLATE_PROPERTY_LINKED_TYPES in propertyValue:
                for linked_type in propertyValue[TEMPLATE_PROPERTY_LINKED_TYPES]:
                    propertyValue["typeInformation"].append({"embedded": False, "type": os.path.basename(linked_type)})
            elif TEMPLATE_PROPERTY_EMBEDDED_TYPES in propertyValue:
                for embeddedType in propertyValue[TEMPLATE_PROPERTY_EMBEDDED_TYPES]:
                    propertyValue["typeInformation"].append({"embedded": True, "type": os.path.basename(embeddedType)})
        return schema

    def generate(self, ignore=None):
        super().generate(ignore=ignore)
        overall = "@startuml\n"
        for written_file in self.written_files:
            with open(written_file, "r") as file:
                data = file.read()
            data = data.replace("@startuml", "")
            data = data.replace("@enduml", "")
            overall += data
        overall += "\n@enduml"
        overall_file = os.path.join(self.target_path, "overall.uml")
        overall_target = os.path.join(self.target_path, "overall.svg")
        with open(overall_file, "w") as overall_file:
            overall_file.write(overall)

if __name__ == "__main__":
    PlantUMLGenerator([]).generate()
