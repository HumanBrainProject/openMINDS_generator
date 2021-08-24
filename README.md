<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator-logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator-logo.png" alt="openMINDS generator logo" title="openMINDS generator" align="right" height="70" />
</a>

# Welcome to openMINDS!

This is the repository for the generator scripts of
[**openMINDS**](https://github.com/HumanBrainProject/openMINDS)

These scripts allow the generation of the output formats HTML, schema.json and
python from the template language used to define the openMINDS schemas.

In addition to this the python compiler allows the dynamic usage of openMINDS
in your Python appication.

Example:

    import generator.openminds_helper
    import generator.python_compiler


    helper = generator.openminds_helper.OpenMINDS_helper()
    copyright = generator.python_compiler.generate(helper.core.DATA__COPYRIGHT)
    copyright_schema = generator.python_compiler.generate_file(helper.core.DATA__COPYRIGHT)

    copyright_schema.year = 2020
    copyright_schema.holder = "somebody"

    copyright_schema.save("test.json")

This example generates a copyright schema object, for which the values can be
set and it can be saved as openMINDS conform json.

## License
This work is licensed under the MIT License.
