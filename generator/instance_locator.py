import glob
import json
import os
from generator.commons import find_resource_directories, INSTANCE_FILE_ENDING


class InstanceLocator(object):

    def __init__(self, path):
        self.root_path = os.path.realpath(path)

    def find_instances(self) -> dict:
        instances_by_type = {}
        for instance_dir in find_resource_directories(self.root_path, file_ending=INSTANCE_FILE_ENDING, ignore=["tests"]):
            submodule = instance_dir.split("/")[0]
            version_path = os.path.join(self.root_path, submodule, "version.txt")
            if os.path.isfile(version_path):
                with open(version_path, "r") as version_file:
                    version = version_file.read().strip()
            else:
                version = "v0"

            for instance_path in glob.glob(os.path.join(self.root_path, instance_dir, f'**/*{INSTANCE_FILE_ENDING}'), recursive=True):
                with open(instance_path, "r") as instance_file:
                    try:
                        payload = json.load(instance_file)
                    except json.decoder.JSONDecodeError as e:
                        print(f"Can't process {instance_path} since it contains a syntax error - {e}")
                        continue
                if "@type" not in payload or "@id" not in payload:
                    print(f"Can't process {instance_path} since it doesn't contain both @type and @id")
                    continue
                types = payload["@type"]
                if types and type(types) is not list:
                    types = [types]
                relative_path = instance_path[len(f"{self.root_path}/{submodule}/"):]

                structure = {
                    "id": payload["@id"],
                    "relativePath": relative_path,
                    "githubUrl": f"https://raw.githubusercontent.com/HumanBrainProject/openMINDS_{submodule}/{version}/{relative_path}",
                    "label": payload["name"] if "name" in payload else payload["shortName"] if "shortName" in payload else payload["lookupLabel"] if "lookupLabel" in payload else None, #TODO make this dynamic
                    "interlex": payload["interlexIdentifier"] if "interlexIdentifier" in payload else None,
                    "knowledgeSpace": payload["knowledgeSpaceLink"] if "knowledgeSpaceLink" in payload else None,
                    "ontologyIdentifier": payload["preferredOntologyIdentifier"] if "preferredOntologyIdentifier" in payload else None,
                    "extraInfo": payload["definition"] if "definition" in payload else payload["versionIdentifier"] if "versionIdentifier" in payload else payload["internalIdentifier"] if "internalIdentifier" in payload else None
                }
                for t in types:
                    if t not in instances_by_type:
                        instances_by_type[t] = []
                    instances_by_type[t].append(structure)
        return instances_by_type
