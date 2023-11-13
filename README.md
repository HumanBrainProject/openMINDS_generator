# WARNING: DEPRECATED REPOSITORY

**openMINDS moved now to a new GitHub organization: https://github.com/openMetadataInitiative**  

**This movement led to a couple of changes. SUMMARY OF CHANGES:**
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS
  + branch 'main' contains vocabulary and fully extended openMINDS schemas in openMINDS syntax
  + fully extended openMINDS schemas in openMINDS syntax use the extension `*.schema.omi.json`
  + schemas are build for openMINDS versions in dedicated folders in branch 'main'
  + code for gathering and extending schemas in the main branch is located in branch 'pipeline'
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS_json-schema
  + branch 'main' contains extended openMINDS schemas (per openMINDS version) formatted in JSON-Schema
  + code for reformmating schemas is located in branch 'pipeline'
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS_instances
  + branch 'main' contains libraries of controlled metadata instances and graph structures for selected schemas across openMINDS metadata models
  + instances and graph strucutres are build for openMINDS versions in dedicated folders in branch 'main'
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS_Python
  + branch 'main' contains extended openMINDS schemas (per openMINDS version) coded as Python classes plus other code for openMINDS Python package
  + code for building openMINDS schema classes is located in branch 'pipeline'
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS_MATLAB
  + branch 'main' contains extended openMINDS schemas (per openMINDS version) coded as Python classes plus other code for openMINDS MATLAB package
  + code for building openMINDS schema classes is located in branch 'pipeline'
+ :arrow_right: https://github.com/openMetadataInitiative/openMINDS_documentation
  + builds the documentation for openMINDS on Read-The-Docs (https://openminds-documentation.readthedocs.io)

<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-generator_logo.png" alt="openMINDS generator logo" title="openMINDS generator" align="right" height="70" />
</a>

# openMINDS_generator!

The openMINDS_generator repository is part of the **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures (openMINDS). It contains the **openMINDS integration pipeline** which builts the main [openMINDS](https://github.com/HumanBrainProject/openMINDS) GitHub repository, the central access point to all openMINDS metadata models for all versions. 

As such, it interprets and exends the openMINDS schema syntax to formal, well-known formats, such as JSON-Schema or HTML, as well as extracts the vocabulary used across all metadata models. All schemas in all supported formats and the vocabulary are stored for central maintenance on the main openMINDS repository. Note that the pipeline is configured in such a way, that each commit on one of the openMINDS submodules will trigger a new build of the main openMINDS repository ensuring that its content is always up-to-date.

The openMINDS_generator repository also hosts a small **openMINDS Python** library which allows you the dynamic usage of openMINDS in your Python application. Please find below a small documenation on how to install and use openMINDS Python.

For more technical details please go to the [central openMINDS repository](https://github.com/HumanBrainProject/openMINDS) or the [openMINDS Collab](https://wiki.ebrains.eu/bin/view/Collabs/openminds/).

<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-python-logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/light_openMINDS-python-logo.png" alt="openMINDS Python logo" title="openMINDS Python" align="right" height="50" />
</a>

## openMINDS Python

openMINDS Python is a small library that allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs.

Please note that openMINDS Python only helps you to generate correctly formatted JSON-LD metadata instances - the preparation on how you want to describe your research product with openMINDS is still up to you. If you need support in designing your own openMINDS metadata collection, check out the [openMINDS Collab Tutorials](https://wiki.ebrains.eu/bin/create/openminds%40ebrains/eu/WebHome?parent=Collabs.openminds.Documentation.Application+details.WebHome) which might give you hints on how to tackle your individual case or, of course, get in touch with us directly via our support-email (**`openminds@ebrains.eu`**).

### Installation
The official versions are available at the [Python Package Index](https://pypi.org/project/openMINDS/) and can be installed using pip install in your console:
    
    pip install openMINDS
    
The latest unstable version is available on this GitHub.

### Usage

As stated above, the openMINDS Python allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs. Here a small example:

```python
# Import openMINDS and version manager
import openMINDS
import openMINDS.version_manager

# Initialise a local copy of openMINDS
openMINDS.version_manager.init()

# Select which version of openMINDS to use
openMINDS.version_manager.version_selection('v2.0.0')

# initiate the helper class for the dynamic usage of a specific openMINDS version
helper = openMINDS.Helper()

# initiate the collection into which you will store all metadata instances
mycollection = helper.create_collection()

# create a metadata instance for (e.g.) the openMINDS Person schema
person_open = mycollection.add_core_person(givenName="open")

# add more metadata to a created instance
mycollection.get(person_open).familyName = "MINDS"

# add connections to other metadata instances
email_openminds = mycollection.add_core_contactInformation(email="openminds@ebrains.eu")
mycollection.get(person_open).contactInformation = email_openminds

# save your collection
mycollection.save("./myFirstOpenMINDSMetadataCollection/")

```

This example generates two linked JSON-LDs, one conform with the openMINDS (v3) Person schema and the other conform with the openMINDS (v3) ContactInformation schema.

To learn in general about the available openMINDS metadata models, schemas and their required or optional metadata properties, check out the [openMINDS HTML views](https://humanbrainproject.github.io/openMINDS/) which are deployed as GitHub pages on the main openMINDS repository. You can also have a look at the full [openMINDS documentation](https://wiki.ebrains.eu/bin/view/Collabs/openminds/) on the EBRAINS Collaboratory.

Within the openMINDS Python you can also get an overview of the requirements of a schema and all its properties by using the 'help_X' function. Here an example:

```python
# Getting help for expected schema properties
mycollection.help_core_actors_person()
```


## License
This work is licensed under the MIT License.
