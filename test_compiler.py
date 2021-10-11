import openMINDS.compiler

helper = openMINDS.compiler.Helper()
mycollection = helper.create_collection()
lyuba = mycollection.add_core_person(givenName="Lyuba")
mycollection.help_core_data_copyright()
mycollection.get(lyuba).familyName = "Zehl"
email_lyuba = mycollection.add_core_contactInformation(email="openminds@ebrains.eu")
mycollection.get(lyuba).contactInformation = email_lyuba
mycollection.save("./myFirstOpenMINDSMetadataCollection/")


#import openMINDS.compiler


#helper = openMINDS.compiler.Helper()

#container = helper.get_container()
#file_1 = container.add_core_data_fileInstance("name", "IRI", "partof")
#print(file_1)
#print(container.get(file_1).get_name())
#container.get(file_1).set_name("new_name")
#help(container)
#print(container.get(file_1).get_name())
#help(container.get(test))
#container.get(file_1).set_storageSize(None)
#container.save("./metadata/")
#container.add_core_data_fileInstance("name", "IRI", "isPartOf")
#container.save("./metadata/")
