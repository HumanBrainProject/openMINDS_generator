import os
from typing import List, Dict

from generator.commons import JinjaGenerator, TEMPLATE_PROPERTY_TYPE, \
    TEMPLATE_PROPERTY_LINKED_TYPES, SchemaStructure, TEMPLATE_PROPERTY_EMBEDDED_TYPES


class HTMLGenerator(JinjaGenerator):

    def __init__(self, schema_information:List[SchemaStructure]):
        super().__init__("html", ["html", "xml"], "documentation_template.html")
        self.schema_information = schema_information
        self.schema_information_by_type = {}
        self.schema_collection_by_group = {}
        for s in self.schema_information:
            self.schema_information_by_type[s.type] = s

    def _schema_info_to_rel_url(self, schema_info):
        return schema_info.file.replace("tpl.json", "json")

    def _schema_info_to_rel_html_url(self, schema_info):
        return f"../../../../{schema_info.schema_group}/{schema_info.version}/{schema_info.file.replace('schema.tpl.json', 'html')}"

    def _pre_process_template(self, schema):
        schema_information = self.schema_information_by_type[schema[TEMPLATE_PROPERTY_TYPE]]
        schema["simpleTypeName"] = os.path.basename(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaId"] = self._schema_info_to_rel_url(schema_information)
        schema["schemaGroup"] = schema_information.schema_group.split("/")[0]
        schema["schemaVersion"] = schema_information.version
        for property, propertyValue in schema["properties"].items():
            if TEMPLATE_PROPERTY_LINKED_TYPES in propertyValue:
                propertyValue["typeInformation"] = []
                for linked_type in propertyValue[TEMPLATE_PROPERTY_LINKED_TYPES]:
                    linked_type_info = self.schema_information_by_type[linked_type]
                    propertyValue["typeInformation"].append({"url": self._schema_info_to_rel_html_url(linked_type_info),
                                                             "label": os.path.basename(linked_type)})
            elif TEMPLATE_PROPERTY_EMBEDDED_TYPES in propertyValue:
                propertyValue["typeInformation"] = []
                for embedded_type in propertyValue[TEMPLATE_PROPERTY_EMBEDDED_TYPES]:
                    embedded_type_info = self.schema_information_by_type[embedded_type]
                    propertyValue["typeInformation"].append({"url": self._schema_info_to_rel_html_url(embedded_type_info),
                                                             "label": f"{os.path.basename(embedded_type)} (embedded)"})
            elif "type" in propertyValue and "format" in propertyValue:
                propertyValue["typeInformation"] = [{"label": f"{propertyValue['type']} ({propertyValue['format']})"}]
            elif "type" in propertyValue:
                propertyValue["typeInformation"] = [{"label": propertyValue['type']}]
            else:
                propertyValue["typeInformation"] = [{"label": "unknown"}]
        if schema["schemaGroup"] not in self.schema_collection_by_group:
            self.schema_collection_by_group[schema["schemaGroup"]] = []
        self.schema_collection_by_group[schema["schemaGroup"]].append(schema_information)
        return schema

    def generate(self):
        super().generate()
        group_templ = self.env.get_template("group_template.html")
        for group in self.schema_collection_by_group.keys():
            group_schema = {
                "group": group,
                "types": []
            }
            for schema in self.schema_collection_by_group[group]:
                group_schema["types"].append({"name": os.path.basename(schema.type), "url": f"{schema.schema_group.split('/')[0]}/schemas/{schema.version}/{schema.file.replace('schema.tpl.json', 'html')}"})

            group_schema["types"] = sorted(group_schema["types"], key= lambda type: type["name"])
            html = group_templ.render(group_schema)
            with open(os.path.join(self.target_path, f"{group}.html"), "w") as group_file:
                group_file.write(html)
        root_templ = self.env.get_template("root_template.html")
        root_model = {
            "modules": sorted([m for m in self.schema_collection_by_group.keys()], key=str.casefold)
        }
        root_html = root_templ.render(root_model)
        with open(os.path.join(self.target_path, f"index.html"), "w") as root_file:
            root_file.write(root_html)

if __name__ == "__main__":
    HTMLGenerator([]).generate()
