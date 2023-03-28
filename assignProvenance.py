import os
import synapseclient
from synapseclient import Project, Folder, File, Link, Activity

syn = synapseclient.Synapse()
  
def setCompleteProvenanceStudy (username, password, study, geneCountsTableSynID, MODELADHarmonizationSynID):
  syn.login(username, password)
  
  # pull metadata syn ids
  studyQuoted = "'" + study + "'"
  
  query = syn.tableQuery("SELECT * FROM syn11346063.34 WHERE ( ( \"metadataType\" = 'assay' OR \"metadataType\" = 'biospecimen' OR \"metadataType\" = 'individual' ) AND ( \"study\" HAS ( " + studyQuoted + " ) ) )")
  metadataManifest = query.asDataFrame()
  
  synidBiospecimen = metadataManifest[metadataManifest['name'].str.contains('biospecimen')]['id'].values[0]
  synidIndividual = metadataManifest[metadataManifest['name'].str.contains('individual')]['id'].values[0]
  
  act = Activity(name='process differential expression', description='calculate stratified differential expresssion table csvs')
  act.used([geneCountsTableSynID, synidBiospecimen, synidIndividual])
  act.executed('https://github.com/j-hendrickson-sage/generalCaseRNASeqAnalysis/blob/main/generalCaseRNASeqAnalysis.Rmd')
  
  data_folder = Folder(study, MODELADHarmonizationSynID)
  data_folder = syn.store(data_folder)

  for x in os.listdir('UCI_3xTg-AD'):
    entity = File(study + '/' + x, description='differential expression', parent=data_folder)
    entity = syn.store(entity, activity=act)
