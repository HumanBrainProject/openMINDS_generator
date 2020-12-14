import sys
import json
import requests
import jsonschema

dict_schema_resolver = {
    "AnatomicalEntity": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/anatomicalEntity.schema.json",
    "AnatomicalEntityRelation": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/anatomicalEntityRelation.schema.json",
    "Annotation": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/annotation.schema.json",
    "AtlasTerminology": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/atlasTerminology.schema.json",
    "BrainAtlas": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/brainAtlas.schema.json",
    "BrainAtlasVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/brainAtlasVersion.schema.json",
    "CoordinatePoint": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/coordinatePoint.schema.json",
    "CoordinateSpace": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/coordinateSpace.schema.json",
    "Electrode": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrode.schema.json",
    "ElectrodeArray": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrodeArray.schema.json",
    "ElectrodeContact": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/electrodeContact.schema.json",
    "Image": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/SANDS/v1/schema.json/image.schema.json",
    "Contribution": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/contribution.schema.json",
    "Organization": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/organization.schema.json",
    "Person": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/actors/person.schema.json",
    "ContentType": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/contentType.schema.json",
    "Copyright": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/copyright.schema.json",
    "FileBundle": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileBundle.schema.json",
    "FileInstance": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileInstance.schema.json",
    "FileRepository": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/fileRepository.schema.json",
    "Hash": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/hash.schema.json",
    "Schema": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/data/license.schema.json",
    "DigitalIdentifier": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/digitalIdentifier.schema.json",
    "DigitalIdentifierSchema": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/digitalIdentifierSchema.schema.json",
    "Funding": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/funding.schema.json",
    "QuantitativeValue": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/quantitativeValue.schema.json",
    "QuantitativeValueRange": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/miscellaneous/quantitativeValueRange.schema.json",
    "Dataset": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/dataset.schema.json",
    "DatasetVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/datasetVersion.schema.json",
    "MetaDataModel": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/metaDataModel.schema.json",
    "MetaDataModelVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/metaDataModelVersion.schema.json",
    "Model": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/model.schema.json",
    "ModelVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/modelVersion.schema.json",
    "Project": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/project.schema.json",
    "Software": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/software.schema.json",
    "SoftwareVersion": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/products/softwareVersion.schema.json",
    "ParameterSetting": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/parameterSetting.schema.json",
    "Protocol": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/protocol.schema.json",
    "ProtocolExecution": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/protocolExecution.schema.json",
    "Subject": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subject.schema.json",
    "SubjectGroup": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectGroup.schema.json",
    "SubjectGroupState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectGroupState.schema.json",
    "SubjectState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/subjectState.schema.json",
    "TissueSample": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSample.schema.json",
    "TissueSampleCollection": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleCollection.schema.json",
    "TissueSampleCollectionState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleCollectionState.schema.json",
    "TissueSampleState": "https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/openMINDS/core/v3/schema.json/research/tissueSampleState.schema.json"
}

def main(json_ld_filename):
    print(json_ld_filename)
    with open(json_ld_filename, 'r') as json_ld_file:
        data = json.load(json_ld_file)
        print(data)
        print(data["@type"].split("/")[-1])
        print(dict_schema_resolver[data["@type"].split("/")[-1]])
        schema = json.loads(requests.get(dict_schema_resolver[data["@type"].split("/")[-1]]).text)
        jsonschema.validate(instance=data, schema=schema)

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
