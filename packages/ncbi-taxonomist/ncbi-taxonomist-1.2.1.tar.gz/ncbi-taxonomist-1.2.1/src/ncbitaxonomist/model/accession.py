"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping


import ncbitaxonomist.model.datamodel

class Accession(ncbitaxonomist.model.datamodel.DataModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__('accs', attributes=attributes)
    attributes = ncbitaxonomist.model.datamodel.standardize_attributes(attributes)
    self.taxonid = ncbitaxonomist.model.datamodel.int_attribute(attributes.pop('taxid', None))
    self.uid = ncbitaxonomist.model.datamodel.int_attribute(attributes.pop('uid', None))
    self.db = attributes.pop('db', None)
    self.accessions = attributes.pop('accessions', {})

  def update_accessions(self, accession:Mapping[str,str]):
    """Update accessions from dictionary with structure accession:type"""
    self.accessions.update(accession)

  def get_attributes(self) -> Dict[str,any]:
    return {'taxid':self.taxonid, 'accessions':self.accessions, 'db':self.db,
            'uid':self.uid}

  def get_accessions(self)->Dict[str,str]:
    """Return accessions as dictionary"""
    return self.accessions
