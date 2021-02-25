import json

def _get_required_properties_list(schema):
    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())

        required_properties = schema_dictionary["required"]
        required_properties.remove("@id")
        required_properties.remove("@type")

        return required_properties

def get_constructor_params(schema):
    required_properties = _get_required_properties_list(schema)
    param_str = ""

    for property in required_properties:
        param_str += property + ", "

    return param_str

def _build_adder_string(schema_dict):
    required_properties = get_constructor_params(schema_dict)
    signature = "add_" + schema_dict["namespace"] + "_" + schema_dict["name"]

    function_string = "def " + signature + "(self, " + required_properties + "):\n"
    function_string += "\timport openMINDS.python_compiler\n"
    function_string += "\tschema_object = openMINDS.python_compiler.generate(" + str(schema_dict) + ")(" + required_properties + ")\n"
    function_string += "\tself.data[schema_object.at_id] = schema_object\n"
    function_string += "\treturn schema_object.at_id\n"

    return (signature, function_string)


def build_adder(schema_dict):
    d = {}
    signature, function_string = _build_adder_string(schema_dict)
    exec(function_string, d)

    return(signature,(d[signature]))


def _build_generator_string(schema_dict):
    required_properties = get_constructor_params(schema_dict)
    signature = schema_dict["namespace"] + "_" + schema_dict["substructure"] + "_" + schema_dict["name"]

    function_string = "def " + signature + "(self, " + required_properties + "):\n"
    function_string += "\timport openMINDS.python_compiler\n"
    function_string += "\tschema_object = openMINDS.python_compiler.generate(" + str(schema_dict) + ")(" + required_properties + ")\n"
    function_string += "\treturn schema_object\n"

    return (signature, function_string)

def build_generator(schema_dict):
    d = {}
    signature, function_string = _build_generator_string(schema_dict)
    exec(function_string, d)

    return(signature,(d[signature]))


def _build_constructor_string():
    out_str = "def __init__(self, core, SANDS):\n"
    out_str += "\tself.data = {}\n"

    return out_str


def build_constructor():
    d = {}
    exec(_build_constructor_string(), d)

    return(d['__init__'])


def _build_save_string():
    out_str = "def save(self, output_folder):\n"
    out_str += "\tfor item in self.data.values():\n"
    out_str += "\t\titem.save(output_folder)\n"

    return out_str


def build_save():
    d = {}
    exec(_build_save_string(), d)

    return(d['save'])


def _build_get_string():
    out_str = "def get(self, id):\n"
    out_str += "\treturn self.data[id]\n"

    return out_str


def build_get():
    d = {}
    exec(_build_get_string(), d)

    return(d['get'])


def _build_help_string(schema):
    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())

        signature = schema["namespace"] + "_" + schema["substructure"] + "_" + schema["name"]
        signature = "help_" + signature
        function_string = "def " + signature + "(self):\n"

        required_properties = _get_required_properties_list(schema)
        function_string += '\tprint("Required properties:")\n'
        for property in required_properties:
            function_string += '\tprint("' + property + '")\n'
        function_string += '\tprint("")\n'

        for property in schema_dictionary["properties"]:
            try:
                instruction = schema_dictionary["properties"][property]["_instruction"]
            except:
                #print("No instruction found for: " + str(property))
                instruction = "Not defined yet."

            try:
                description = schema_dictionary["properties"][property]["description"]
            except:
                #print("No description found for: " + str(property))
                description = "Not defined yet."

            function_string += '\tprint("Documentation of ' + property +'")\n'
            function_string += '\tprint("INSTRUCTION:")\n'
            function_string += '\tprint("' + instruction + '")\n'
            function_string += '\tprint("")\n'
            function_string += '\tprint("DESCRIPTION:")\n'
            function_string += '\tprint("' + description + '")\n'
            function_string += '\tprint("")\n'

        func = {"signature": signature, "function_string": function_string}
        return func

def build_help(schema):
    d = {}
    func = _build_help_string(schema)
    exec(func["function_string"], d)

    return(func["signature"], d[func["signature"]])
