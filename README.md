# openMINDS_generator

The **openMINDS_generator** is part of the open Metadata Initiative for Neuroscience Data Structures ([**openMINDS**](https://github.com/HumanBrainProject/openMINDS)). It contains scripts that interpret and extend the openMINDS schema template language as well as translate the openMINDS schema templates to various formal output formats (e.g., HTML and JSON-Schema). 

Moreover, the openMINDS_generator includes a small compiler that enables the dynamic usage of the openMINDS schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs. 

### Installation

The **openMINDS Python API** is also available at the [Pyhton Package Index](https://pypi.org/project/openMINDS/) and can be installed using `pip install` in your console:

```console
pip install openMINDS
```

### Documentation

#### openMINDS Python API

As stated above, the openMINDS.compiler allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs. Here a small example:

```python
import openMINDS.compiler

# initiate the helper class for the dynamic usage of a specific openMINDS version
helper = openMINDS.compiler.Helper(version="dev")

# initiate the collection into which you will store all metadata instances
mycollection = helper.create_collection()

# create a metadata instance for (e.g.) the openMINDS Person schema
lyuba = mycollection.add_core_person(givenName="Lyuba")

# add more metadata to a created instance
mycollection.get(lyuba).familyName = "Zehl"

# add connections to other metadata instances
email_lyuba = mycollection.add_core_contactInformation(email="openminds@ebrains.eu")
mycollection.get(lyuba).contactInformation = email_lyuba

# save your collection
mycollection.save("./myFirstOpenMINDSMetadataCollection/")
```

To learn in general about the available openMINDS metadata models, schemas and their required or optional metadata properties, please go the [main openMINDS GitHub repository](https://github.com/HumanBrainProject/openMINDS), or the full documentation on the EBRAINS Collaboratory (coming soon).

Within the openMINDS.compiler you can also get an overview of the requirement of a schema and all its properties by using the `help_X` function. Here an example:

```python
mycollection.help_core_person()
```

## License
This work is licensed under the MIT License.
