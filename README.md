<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png" alt="openMINDS generator logo" title="openMINDS generator" align="right" height="70" />
</a>

# openMINDS_generator!

The openMINDS_generator repository is part of the **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures (openMINDS). It contains the **openMINDS integration pipeline** which builts the main [openMINDS](https://github.com/HumanBrainProject/openMINDS) GitHub repository, the central access point to all openMINDS metadata models for all versions. 

As such, it interprets and exends the openMINDS schema syntax to formal, well-known formats, such as JSON-Schema or HTML, as well as extracts the vocabulary used across all metadata models. All schemas in all supported formats and the vocabulary are stored for central maintenance on the main openMINDS repository. Note that the pipeline is configured in such a way, that each commit on one of the openMINDS submodules will trigger a new build of the main openMINDS repository ensuring that its content is always up-to-date.

The openMINDS_generator repository also hosts a small **openMINDS Python** library which allows you the dynamic usage of openMINDS in your Python application.

For more technical details please go to the [central openMINDS repository](https://github.com/HumanBrainProject/openMINDS) or the [openMINDS Collab](https://wiki.ebrains.eu/bin/view/Collabs/openminds/).

<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-python_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-python_logo.png" alt="openMINDS Python logo" title="openMINDS Python" align="right" height="50" />
</a>

## openMINDS Python

openMINDS Python is a small library that allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs.

Please note that openMINDS Python only helps you to generate correctly formatted JSON-LD metadata instances - the preparation on how you want to describe your research product with openMINDS is still up to you. If you need support in designing your own openMINDS metadata collection, check out the [openMINDS Collab Tutorials](https://wiki.ebrains.eu/bin/create/openminds%40ebrains/eu/WebHome?parent=Collabs.openminds.Documentation.Application+details.WebHome) which might give you hints on how to tackle your individual case or, of course, get in touch with us directly via **`openminds@ebrains.eu`**.

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
