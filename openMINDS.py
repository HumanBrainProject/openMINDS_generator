import argparse
import os
import shutil
import sys

from generator.commons import TARGET_PATH
from generator.expander import Expander
from generator.generate_html import HTMLGenerator
from generator.generate_json_schema import JsonSchemaGenerator
from generator.generate_python import generate_all_schemas

parser = argparse.ArgumentParser(prog=sys.argv[0], description='Generate various sources out of the EBRAINS openMINDS schema templates')
parser.add_argument('--version', help="The version of the current build", required=True)
args = vars(parser.parse_args())


def main():
    version = args["version"]
    print("***************************************")
    print(f"Triggering the generation of sources for version {version}...")
    print("***************************************")
    print()
    print("Expanding the schemas...")
    Expander().expand()
    print("Clear target directory")
    if os.path.exists(TARGET_PATH):
        shutil.rmtree(TARGET_PATH)
    print(f"Generating JSON schemas for...")
    JsonSchemaGenerator(version).generate()
    print("Generating HTML documentation...")
    HTMLGenerator(version).generate()
    print("Generating Python classes...")
    generate_all_schemas()


if __name__ == "__main__":
    main()
