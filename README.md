<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png" alt="openMINDS generator logo" title="openMINDS generator" align="right" height="70" />
</a>

# openMINDS_generator!

The openMINDS_generator repository is part of the **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures (openMINDS). It contains the openMINDS integration pipeline which builts the main [openMINDS](https://github.com/HumanBrainProject/openMINDS) GitHub repository, the central access point to all openMINDS metadata models for all versions. As such, it interprets and exends the openMINDS schema syntax to formal, well-known formats, such as JSON-Schema or HTML, as well as extracts the vocabulary used across all metadata models. All schemas in all supported formats and the vocabulary are stored for central maintenance on the main openMINDS repository.

Note that the pipeline is configured in such a way, that each commit on one of the openMINDS submodules will trigger a new build of the main openMINDS repository ensuring that its content is always up-to-date.

In addition, the openMINDS_generator hosts a small openMINDS Python library which allows you the dynamic usage of openMINDS in your Python application.

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
