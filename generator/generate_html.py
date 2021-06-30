import os
from typing import List, Dict

from generator.commons import JinjaGenerator, TEMPLATE_PROPERTY_TYPE, \
    TEMPLATE_PROPERTY_LINKED_TYPES, SchemaStructure, TEMPLATE_PROPERTY_EMBEDDED_TYPES


class HTMLGenerator(JinjaGenerator):

    def __init__(self, schema_information:List[SchemaStructure], instances, current, all_version_branches, all_tags):
        super().__init__("html", ["html", "xml"], "documentation_template.html")
        self.schema_information = schema_information
        self.schema_information_by_type = {}
        self.schema_collection_by_group = {}
        self.current = current
        self.instances = instances
        self.all_version_branches = all_version_branches
        self.all_tags = all_tags
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "style.css"), "r", encoding="utf-8") as style_file:
            self.style = style_file.read()
        for s in self.schema_information:
            self.schema_information_by_type[s.type] = s

    def _schema_info_to_rel_url(self, schema_info):
        return schema_info.file.split("/")[-1].replace("tpl.json", "json")

    def _schema_info_to_rel_html_url(self, current_schema_info, schema_info):
        number_of_relative_levels = len(f"{current_schema_info.schema_group}/{current_schema_info.version}/{current_schema_info.file}".split("/"))-1
        return f"{'../'*number_of_relative_levels}{schema_info.schema_group}/{schema_info.version}/{schema_info.file.replace('schema.tpl.json', 'html')}"

    def _pre_process_template(self, schema):
        schema_information = self.schema_information_by_type[schema[TEMPLATE_PROPERTY_TYPE]]
        schema["simpleTypeName"] = os.path.basename(schema[TEMPLATE_PROPERTY_TYPE])
        schema["schemaId"] = self._schema_info_to_rel_url(schema_information)
        schema["schemaGroup"] = schema_information.schema_group.split("/")[0]
        schema["schemaVersion"] = schema_information.version
        schema["style"] = self.style
        if schema[TEMPLATE_PROPERTY_TYPE] in self.instances:
            schema["instances"] = sorted(self.instances[schema[TEMPLATE_PROPERTY_TYPE]], key=lambda k: k["label"])
        sorted_keys = sorted(schema["properties"].keys())

        for property in sorted_keys:
            property_value = schema["properties"][property]
            property_value["is_required"] =  property in schema["required"] if "required" in schema else False
            property_value["embedded"] = False
            property_value["linked"] = False
            property_value["is_array"] = False
            property_value["typeInformation"] = []
            if "type" in property_value and property_value["type"] == "array":
                property_value["is_array"] = True
                property_value["cardinality"] = f"({property_value['minItems'] if 'minItems' in property_value else 0} - {property_value['maxItems'] if 'maxItems' in property_value else 'n'})"
                if "items" in property_value:
                    if "type" in property_value["items"]:
                        label = f"{property_value['items']['type']}"
                    else:
                        label = ""
                    if '_formats' in property_value['items']:
                        formats = f" (format: {' or '.join(property_value['items']['_formats'])})"
                    else:
                        formats = ""
                    property_value["typeInformation"].append({"label": f"{label}{formats}"})
                elif TEMPLATE_PROPERTY_LINKED_TYPES in property_value:
                    property_value["linked"] = True
                    for linked_type in property_value[TEMPLATE_PROPERTY_LINKED_TYPES]:
                        if linked_type in self.schema_information_by_type:
                            linked_type_info = self.schema_information_by_type[linked_type]
                            property_value["typeInformation"].append({"url": self._schema_info_to_rel_html_url(schema_information, linked_type_info),
                                                                     "label": os.path.basename(linked_type)})
                        else:
                            property_value["typeInformation"].append({"url": None,
                                                                      "label": f"Unknown type: {linked_type}"})

                elif TEMPLATE_PROPERTY_EMBEDDED_TYPES in property_value:
                    property_value["embedded"] = True
                    for embedded_type in property_value[TEMPLATE_PROPERTY_EMBEDDED_TYPES]:
                        if embedded_type in self.schema_information_by_type:
                            embedded_type_info = self.schema_information_by_type[embedded_type]
                            property_value["typeInformation"].append({"url": self._schema_info_to_rel_html_url(schema_information, embedded_type_info),
                                                                     "label": f"{os.path.basename(embedded_type)}"})
                        else:
                            property_value["typeInformation"].append({"url": None,
                                                                  "label": f"Unknown type: {embedded_type}"})

                else:
                    property_value["typeInformation"].append({"label": "unknown"})
            elif "type" in property_value and property_value["type"] != "array":
                if "_formats" in property_value:
                    property_value["typeInformation"].append({"label": f"{property_value['type']} (format: {' or '.join(property_value['_formats'])})"})
                else:
                    property_value["typeInformation"].append({"label": property_value['type']})
            elif "type" not in property_value:
                if TEMPLATE_PROPERTY_LINKED_TYPES in property_value:
                    property_value["linked"] = True
                    for linked_type in property_value[TEMPLATE_PROPERTY_LINKED_TYPES]:
                        if linked_type in self.schema_information_by_type:
                            linked_type_info = self.schema_information_by_type[linked_type]
                            property_value["typeInformation"].append({"url": self._schema_info_to_rel_html_url(schema_information, linked_type_info),
                                                                     "label": os.path.basename(linked_type)})
                        else:
                            property_value["typeInformation"].append({"url": None,
                                                                      "label": f"Unknown type: {linked_type}"})
                elif TEMPLATE_PROPERTY_EMBEDDED_TYPES in property_value:
                    property_value["embedded"] = True
                    for embedded_type in property_value[TEMPLATE_PROPERTY_EMBEDDED_TYPES]:
                        if embedded_type in self.schema_information_by_type:
                            embedded_type_info = self.schema_information_by_type[embedded_type]
                            property_value["typeInformation"].append({"url": self._schema_info_to_rel_html_url(schema_information, embedded_type_info),
                                                                     "label": f"{os.path.basename(embedded_type)}"})
                        else:
                            property_value["typeInformation"].append({"url": None,
                                                                      "label": f"Unknown type: {embedded_type}"})
                else:
                    property_value["typeInformation"].append({"label": "unknown"})                
            else:
                property_value["typeInformation"].append({"label": "unknown"})
        if schema["schemaGroup"] not in self.schema_collection_by_group:
            self.schema_collection_by_group[schema["schemaGroup"]] = []
        self.schema_collection_by_group[schema["schemaGroup"]].append(schema_information)
        return schema

    def _create_model_for_groups(self, group):
        group_schema = {
            "group": group,
            "style": self.style,
            "typesByCategory": {},
            "allTags": sorted(self.all_tags, reverse=True),
            "allVersions": sorted(self.all_version_branches, reverse=True),
            "current": self.current
        }
        for schema in self.schema_collection_by_group[group]:
            file_split = schema.file.split('/')
            category = file_split[0] if len(file_split) > 1 else ""
            if category not in group_schema["typesByCategory"]:
                group_schema["typesByCategory"][category] = []
            group_schema["typesByCategory"][category].append(
                {"name": f"{os.path.basename(schema.type)}", "url": f"{schema.schema_group}/{schema.version}/{schema.file.replace('schema.tpl.json', 'html')}"})

        for k in group_schema["typesByCategory"]:
            group_schema["typesByCategory"][k] = sorted(group_schema["typesByCategory"][k], key=lambda type: type["name"])
        return group_schema


    def generate(self, ignore=None):
        super().generate(ignore=ignore)
        group_templ = self.env.get_template("group_template.html")
        for group in self.schema_collection_by_group.keys():
            group_schema = self._create_model_for_groups(group)
            html = group_templ.render(group_schema)
            with open(os.path.join(self.target_path, f"{group}.html"), "w", encoding="utf-8") as group_file:
                group_file.write(html)
        root_templ = self.env.get_template("root_template.html")
        root_model = {
            "current": self.current,
            "allTags": sorted(self.all_tags, reverse=True),
            "allVersions": sorted(self.all_version_branches, reverse=True),
            "modules": sorted([{"name": m, "types": self._create_model_for_groups(m)} for m in self.schema_collection_by_group.keys()], key=lambda module: module["name"].casefold()),
            "style": self.style
        }
        root_html = root_templ.render(root_model)
        with open(os.path.join(self.target_path, f"index.html"), "w", encoding="utf-8") as root_file:
            root_file.write(root_html)
        default_content_templ = self.env.get_template("default_content_template.html")
        default_html = default_content_templ.render(root_model)
        with open(os.path.join(self.target_path, f"default.html"), "w", encoding="utf-8") as default_file:
            default_file.write(default_html)

        central_model = {
            "allTags": sorted(self.all_tags, reverse=True),
            "allVersions": sorted(self.all_version_branches, reverse=True),
            "style": self.style
        }
        central_content_templ = self.env.get_template("central_template.html")
        central_html = central_content_templ.render(central_model)
        with open(os.path.join(self.target_path, f"central.html"), "w", encoding="utf-8") as central_file:
            central_file.write(central_html)

if __name__ == "__main__":
    HTMLGenerator([]).generate()
