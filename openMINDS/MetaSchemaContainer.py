import json

def get_constructor_params(schema):
    with open(schema["filename"],'r') as f:
        schema_dictionary = json.loads(f.read())

        required_properties = schema_dictionary["required"]
        required_properties.remove("@id")
        required_properties.remove("@type")

        param_str = ""

        for property in required_properties:
            param_str += property + ", "

        return param_str

def _build_adder_string(schema_dict):

    required_properties = get_constructor_params(schema_dict)
    print(required_properties)

    signature = "add_" + schema_dict["namespace"] + "_" + schema_dict["substructure"] + "_" + schema_dict["name"]
    function_string = "def " + signature + "(self, " + required_properties + "):\n"
    function_string += "\timport openMINDS.python_compiler\n"
    function_string += "\tschema_object = openMINDS.python_compiler.generate(" + str(schema_dict) + ")(" + required_properties + ")\n"
    function_string += "\tself.data[schema_object.at_id] = schema_object\n"
    function_string += "\treturn schema_object.at_id\n"

    return (signature, function_string)


def build_adder(schema_dict):
    d = {}
    signature, function_string = _build_adder_string(schema_dict)
    print(function_string)
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
