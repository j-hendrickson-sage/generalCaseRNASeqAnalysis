import synapseclient
import pandas as pd
import argparse
syn = synapseclient.Synapse()

parser = argparse.ArgumentParser(description='combine biospecimen and individual metadata for Model AD')

parser.add_argument('--username', help='Enter Synapse username')
parser.add_argument('--password', help='enter Synapse password')
parser.add_argument('--study', help='enter study')

args = parser.parse_args()

syn.login(args.username, args.password)

study = args.study
studyQuoted = "'" + study + "'"

query = syn.tableQuery("SELECT * FROM syn11346063.34 WHERE ( ( \"metadataType\" = 'assay' OR \"metadataType\" = 'biospecimen' OR \"metadataType\" = 'individual' ) AND ( \"study\" HAS ( " + studyQuoted + " ) ) )")
metadataManifest = query.asDataFrame()

def getDf (filename, metadataManifest):
  synid = metadataManifest[metadataManifest['name'] == filename]['id'].values[0]
  entity = syn.get(synid)
  df = pd.read_csv(entity.path, sep=",", dtype=str)
  return(df)

def joinMetadata (biospecimenName, individualName, metadataManifest):
  biospecimen_metadata_df = getDf(biospecimenName, metadataManifest)
  individual_human_metadata_df = getDf(individualName, metadataManifest)
  return(pd.merge(biospecimen_metadata_df, individual_human_metadata_df, on="individualID"))

joinedMetadata = joinMetadata(biospecimenName= study + "_biospecimen_metadata.csv", individualName= study + "_individual_metadata.csv", metadataManifest=metadataManifest)

joinedMetadata.to_csv(study + '_joinedMetadata.csv', index=False)
