"""
..
  Copyright 2020 The University of Sydney

  DTDs:
    assembly:
      https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20180216/esummary_assembly.dtd
    bioprojects:
      https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20180216/esummary_assembly.dtd
.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

seqdb_keys = ['accessionversion', 'caption', 'extra']

accessions = {
  'assembly':['assemblyaccession', 'lastmajorreleaseaccession', 'assemblyname'],
  'bioproject':['project_id', 'project_acc', 'project_name'],
  'nucleotide':seqdb_keys,
  'nuccore':seqdb_keys,
  'nucest':seqdb_keys,
  'nucgss':seqdb_keys,
  'popset':seqdb_keys,
  'popset':seqdb_keys,
  'protein':seqdb_keys
}

#attributes = {'taxid' : 'taxonid', 'parent_taxid' : 'parentid', 'rank':'rank'}
attributes = {'taxid' : 'taxid', 'parent_taxid' : 'parentid', 'rank':'rank'}
