import sys
import json
import requests
import jsonschema

dict_schema_resolver = {
    "anatomicalEntity": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/anatomicalEntity.schema.json",
    "anatomicalEntityRelation": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/anatomicalEntityRelation.schema.json",
    "annotation": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/annotation.schema.json",
    "atlasTerminology": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/atlasTerminology.schema.json",
    "brainAtlas": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/brainAtlas.schema.json",
    "brainAtlasVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/brainAtlasVersion.schema.json",
    "coordinatePoint": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/coordinatePoint.schema.json",
    "coordinateSpace": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/coordinateSpace.schema.json",
    "electrode": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrode.schema.json",
    "electrodeArray": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrodeArray.schema.json",
    "electrodeContact": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrodeContact.schema.json",
    "image": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/image.schema.json",
    "contribution": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/contribution.schema.json",
    "organization": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/organization.schema.json",
    "person": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/person.schema.json",
    "contentType": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/contentType.schema.json",
    "copyright": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/copyright.schema.json",
    "fileBundle": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileBundle.schema.json",
    "fileInstance": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileInstance.schema.json",
    "fileRepository": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileRepository.schema.json",
    "hash": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/hash.schema.json",
    "schema": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/license.schema.json",
    "digitalIdentifier": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/digitalIdentifier.schema.json",
    "digitalIdentifierSchema": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/digitalIdentifierSchema.schema.json",
    "funding": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/funding.schema.json",
    "quantitativeValue": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/quantitativeValue.schema.json",
    "quantitativeValueRange": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/quantitativeValueRange.schema.json",
    "dataset": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/dataset.schema.json",
    "datasetVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/datasetVersion.schema.json",
    "metaDataModel": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/metaDataModel.schema.json",
    "metaDataModelVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/metaDataModelVersion.schema.json",
    "model": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/model.schema.json",
    "modelVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/modelVersion.schema.json",
    "project": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/project.schema.json",
    "software": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/software.schema.json",
    "softwareVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/softwareVersion.schema.json",
    "parameterSetting": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/parameterSetting.schema.json",
    "protocol": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/protocol.schema.json",
    "protocolExecution": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/protocolExecution.schema.json",
    "subject": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subject.schema.json",
    "subjectGroup": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectGroup.schema.json",
    "subjectGroupState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectGroupState.schema.json",
    "subjectState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectState.schema.json",
    "tissueSample": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSample.schema.json",
    "tissueSampleCollection": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleCollection.schema.json",
    "tissueSampleCollectionState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleCollectionState.schema.json",
    "tissueSampleState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleState.schema.json"
}

def main(json_ld_filename):
    print(json_ld_filename)
    with open(json_ld_filename, 'r') as json_ld_file:
        data = json.load(json_ld_file)
        print(data)
        print(data["@type"].split("/")[-1])
        print(dict_schema_resolver[data["@type"].split("/")[-1]])

def print_help():
    print("Usage:")
    print("validator <json-ld-file>")

def verify_parameters(argv):
    if len(argv) != 2:
        print("Wrong number of arguments")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    verify_parameters(sys.argv)
    main(sys.argv[1])
