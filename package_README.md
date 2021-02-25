This Python API helps you to interact with the EBRAINS openMINDS metadata models and schemas. It consists of two sub-modules:

The **openMINDS.generator** (coming soon) facilitates the translation of the openMINDS schema template syntax to other established formats, such as HTML and JSON-Schema.

The **openMINDS.compiler** allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs.

#### Installation
The official versions are available at the [Python Package Index](https://pypi.org/project/openMINDS/) and can be installed using `pip install` in your console:
```console
pip install openMINDS
```
The latest version is available on [GitHub](https://github.com/HumanBrainProject/openMINDS_generator).

#### Documentation
Please find in the following a basic documenation on how to use the two submodules (openMINDS.generator and openMINDS.compiler) of the openMINDS Python API. A full documentation can be found on the EBRAINS Collaboratory (coming soon).

##### openMINDS.compiler
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

Within the openMINDS.compiler you can also get an overview of the requirement of a schema and all its properties by using the 'help_X' function. Here an example:
```python
mycollection.help_core_person()
```
