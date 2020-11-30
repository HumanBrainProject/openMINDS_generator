import generator.openminds_helper
import generator.python_compiler
from generator.schema_discovery import Schema_Discovery


def _generate_all(module):
    for key in module.keys():
        generator.python_compiler.generate_file(module[key])


def generate_all_schemas(folder):
    _generate_all(Schema_Discovery(folder).schemas)
