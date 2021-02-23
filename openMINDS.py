import argparse
import os
import shutil
import sys

from generator.commons import TARGET_PATH
from generator.expander import Expander
from generator.generate_html import HTMLGenerator
from generator.generate_json_schema import JsonSchemaGenerator
from generator.generate_plantuml import PlantUMLGenerator
from generator.generate_python import generate_all_schemas

parser = argparse.ArgumentParser(prog=sys.argv[0], description='Generate various sources out of the EBRAINS openMINDS schema templates')
parser.add_argument('--path', help="The path to the source", default=".")
args = vars(parser.parse_args())


def main():
    print("***************************************")
    print(f"Triggering the generation of sources for openMINDS ...")
    print("***************************************")
    print()
    print("Expanding the schemas...")
    schema_information = Expander().expand(args["path"])
    print("Clear target directory")
    if os.path.exists(TARGET_PATH):
        shutil.rmtree(TARGET_PATH)
    print(f"Generating JSON schemas for...")
    JsonSchemaGenerator(schema_information).generate()
    print("Generating HTML documentation...")
    HTMLGenerator(schema_information).generate()
    print("Generating UML documentation...")
    PlantUMLGenerator(schema_information).generate()
    print("Generating Python classes...")
    generate_all_schemas()

if __name__ == "__main__":
    main()
