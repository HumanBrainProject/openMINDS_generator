<a href="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/openMINDS_generator_logo.png">
    <img src="https://github.com/HumanBrainProject/openMINDS_generator/blob/main/img/openMINDS_generator_logo.png" alt="openMINDS logo" title="openMINDS" align="right" height="70" />
</a>

# openMINDS_generator <a name="welcome"/>

The **openMINDS_generator** is part of the **open** **M**etadata **I**nitiative for **N**euroscience **D**ata **S**tructures, short **openMINDS**. It contains the **integration pipeline** which builds the [central openMINDS GitHub repository](https://github.com/HumanBrainProject/openMINDS), as well as a small **Python API** which enables the dynamic usage of the openMINDS schemas in your Python application. 

openMINDS is the umbrella for a set of metadata models that can be used to describe neuroscience research products in graph databases (such as the EBRAINS Knowledge Graph). As research products, openMINDS considers data originating from human/animal studies or simulations (datasets), computational models (models), software tools (software), as well as metadata/data models (metaDataModels).

openMINDS is powered by [HBP](https://www.humanbrainproject.eu) (Human Brain Project) and [EBRAINS](https://ebrains.eu/). However, openMINDS is by design open-source and community-driven, looking for external contributions throughout the neuroscience community. 

Within EBRAINS, the openMINDS metadata models are adopted by the EBRAINS Knowledge Graph and Interactive Brain Atlas. In addition, openMINDS is currently in the process of being adopted by the Japan Brain/MINDS project.

The openMINDS development team currently unites knowledge from the EBRAINS Curation Service, the EBRAINS Knowledge Graph, the EBRAINS Atlas, and the INCF Knowledge Space teams. 

#### What you can find here:
1. [How to contribute](#how-to-contribute) 
2. [openMINDS integration pipeline](#integration-pipeline)
3. [openMINDS Python API](#python-api)
4. [License & acknowledgements](#license-and-acknowledgements)

---

## How to contribute <a name="how-to-contribute"/>

If you have general feedback or a request for a new feature, want to report a bug or have a question, please get in touch with us via our support-email: **`openminds@ebrains.eu`** (not active yet). 

If you spot a bug and know how to fix it, if you want to extend existing schemas and/or metadata models, or develop new schemas and/or metadata models, feel always free to also contribute directly by raising an issue and making a pull request on the respective GitHub repository. 

For more information on how to contribute, please have a look at our [CONTRIBUTING](./CONTRIBUTING.md) document.

[BACK TO TOP](#welcome)

## openMINDS integration pipeline  <a name="integration-pipeline"/>

The setup of the central openMINDS GitHub repository is maintained by the openMINDS integration pipeline. The pipeline is configured in such a way, that each commit on one of the openMINDS submodules hosting a metadata model will trigger a new build of the central openMINDS repository ensuring that its content is always up-to-date. 

In summary, the integration pipeline does the following:
1. It makes sure that each version branch the central openMINDS GitHub repository ingests the correct set of openMINDS metadata models as git-submodules. 
2. It extracts the openMINDS vocabulary (schema types and properties) across all openMINDS versions and stores it on the main branch of the central openMINDS GitHub repository to facilitate central maintenance. The setup also allows to manually enrich this vocabulary with general definitions, human-readable labels, and references to vocabulary of other metadata initiatives.
3. It interprets and extends the simplified openMINDS schema syntax to formal, well-known formats, such as JSON-Schema or HTML, and stores the resulting schema representation for each openMINDS version (stable and development) on the documentation branch of the the central openMINDS GitHub repository which is exposed as a [GitHub page](https://humanbrainproject.github.io/openMINDS/).


[BACK TO TOP](#welcome)

## openMINDS Python API <a name="python-api"/>

The **openMINDS Python API** is also available at the [Pyhton Package Index](https://pypi.org/project/openMINDS/) and can be installed using `pip install` in your console:

```console
pip install openMINDS
```

As stated above, the openMINDS.compiler allows you the dynamic usage of openMINDS metadata models and schemas in your Python application for generating your own collection of openMINDS conform metadata representations (instances) as JSON-LDs. Here a small example:

```python
import openMINDS.compiler

# initiate the helper class for the dynamic usage of a specific openMINDS version
helper = openMINDS.compiler.Helper(version="v2.0.0")

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

To learn in general about the available openMINDS metadata models, schemas and their required or optional metadata properties, please go the [central openMINDS GitHub repository](https://github.com/HumanBrainProject/openMINDS), or the full documentation on the EBRAINS Collaboratory (coming soon).

Within the openMINDS.compiler you can also get an overview of the requirement of a schema and all its properties by using the `help_«X»` function:

```python
mycollection.help_core_person()
```

[BACK TO TOP](#welcome)

## License & acknowledgements <a name="license-and-acknowledgements"/>

openMINDS is licensed under the MIT License.

**Logo:** The openMINDS logo was created by U. Schlegel, based on an original sketch by C. Hagen Blixhavn and feedback by L. Zehl.

The metadata model specifications as well as surrounding code and tools were developed in part or in whole in the Human Brain Project, funded from the European Union’s Horizon 2020 Framework Programme for Research and Innovation under Specific Grant Agreements No. 720270, No. 785907, and No. 945539 (Human Brain Project SGA1, SGA2, and SGA3).

[BACK TO TOP](#welcome)
