import json
import jsonschema
import os.path
import pathlib

from string import Template

PYTHON_OUTPUT_FOLDER = "target/python/"


def _build_output_folder(substructure = None):
    if substructure == None:
        return PYTHON_OUTPUT_FOLDER
    else:
        return PYTHON_OUTPUT_FOLDER + "/" + substructure


def _fix_property_name(property):
    if property[0] == "@":
        return "at_" + property[1:]
    else:
        return property


def _fix_property_names(properties):
    out = []
    for property in properties:
        out.append(_fix_property_name(property))

    return out


def _build_generate_dict_function(schema_dictionary):
    dict_fun_string = "def generate_dict():\n"
    dict_fun_string += "\tobject_dictionary = {}\n"

    for property in schema_dictionary["properties"]:
        dict_fun_string += "\tobject_dictionary['" + property + "'] = self." + property + "\n"

    dict_fun_string += "\treturn dict_fun_string"

def get_constructor_params(schema):
    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())

        required_properties = schema_dictionary["required"]
        required_properties = _fix_property_names(required_properties)
        required_properties.remove("at_id")
        required_properties.remove("at_type")

        return required_properties


def _build_constructor_string(schema_name, schema_namespace, schema_dictionary):
    required_properties = schema_dictionary["required"]
    required_properties = _fix_property_names(required_properties)
    required_properties.remove("at_id")
    required_properties.remove("at_type")

    constructor_string = "def __init__(self "
    for property in required_properties:
        constructor_string += ", " + property

    constructor_string += "): \n"

    for property in required_properties:
        constructor_string += "\tself." + property + " = " + property + " \n"

    constructor_string += '\timport uuid\n'
    constructor_string += '\tself.UUID = uuid.uuid1()\n'
    constructor_string += '\tself.type_name = "' + schema_name + '"\n'
    constructor_string += '\tself.type_namespace = "' + schema_namespace + '"\n'
    constructor_string += '\tself.at_id = "https://localhost/" + self.type_name + "/" + str(self.UUID)\n'
    constructor_string += '\tself.at_type = "https://openminds.ebrains.eu/" + self.type_namespace + "/" + self.type_name.title()\n'

    return constructor_string


def _build_get_dict_string(schema_dictionary):
    get_dict_string = "def get_dict(self):\n"
    get_dict_string += "\tdict = {}\n"
    for property in schema_dictionary["properties"]:
        get_dict_string += '\tdict["' + property + '"] = self.' + _fix_property_name(property) + "\n"

    get_dict_string += "\treturn dict"

    return get_dict_string


def _build_save_string(schema_name):
    save_string  = "def save(self, output_folder):\n"
    save_string += '\timport pathlib\n'
    save_string += '\tpathlib.Path(output_folder + "/" + self.type_name).mkdir(parents=True, exist_ok=True)\n'
    save_string += '\tfile_name = output_folder + self.type_name + "/" + str(self.UUID)\n'
    save_string += '\twith open(file_name, "w") as outfile:\n'
    save_string += '\t\timport json\n'
    save_string += "\t\tjson.dump(self.get_dict(), outfile)\n"

    return save_string


def _indent_function(function_string):
    new_function_string = ""
    for line in range(0, len(function_string)):
        new_function_string += "\t" + function_string[line] + "\n"

    return new_function_string


def build_get_dict(schema_dictionary):
    d = {}
    exec(_build_get_dict_string(schema_dictionary), d)

    return(d['get_dict'])


def build_save(schema_name):
    d = {}
    exec(_build_save_string(schema_name), d)

    return(d['save'])


def build_constructor(schema_name, schema_namespace, schema_dictionary):
    d = {}
    exec(_build_constructor_string(schema_name, schema_namespace, schema_dictionary), d)

    return(d['__init__'])


def generate(schema):
    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())

        jsonschema.Draft7Validator.check_schema(schema_dictionary)

        #class_dictionary = {"__doc__": schema_dictionary["description"]}
        class_dictionary = {}

        for property in schema_dictionary["properties"]:
            class_dictionary[_fix_property_name(property)] = None

        class_dictionary["__init__"] = build_constructor(schema["name"], schema["namespace"], schema_dictionary)
        class_dictionary["get_dict"] = build_get_dict(schema_dictionary)
        class_dictionary["save"] = build_save(schema["name"])

        return type(schema["name"], (object,), class_dictionary)


def generate_file(schema):
    # Check if output-folder exists
    if "substructure" in schema:
        output_folder = _build_output_folder(schema["substructure"])
        if not os.path.exists(output_folder):
            pathlib.Path(output_folder).mkdir(parents=True)
    else:
        output_folder = _build_output_folder()
        if not os.path.exists(output_folder):
            pathlib.Path(output_folder).mkdir(parents=True)

    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())
        template_string = "import json\n\n\n"
        template_string += "class $schema_name:\n"
        constructor_string = _indent_function(_build_constructor_string(schema["name"], schema["namespace"], schema_dictionary).split("\n"))
        get_dict_string = _indent_function(_build_get_dict_string(schema_dictionary).split("\n"))
        save_string = _indent_function(_build_save_string(schema["name"]).split("\n"))

        for property in schema_dictionary["properties"]:
            template_string += "\t" + _fix_property_name(property) + " = None\n"

        # Add constructor
        template_string += "\n$init"
        template_string += "\n$getdict"
        template_string += "\n$save"
        # Prepare template for substitution
        class_string_template = Template(template_string)
        # Print the "file", for now
        out_str = class_string_template.substitute({"schema_name": schema["name"], "init":constructor_string, "getdict": get_dict_string, "save": save_string})

        output_file = output_folder + "/" + schema["name"] + ".py"

        with open(output_file, "w") as outfile:
            outfile.write(out_str)
