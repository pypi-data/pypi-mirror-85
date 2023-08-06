"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping, Type

import ncbitaxonomist.utils
import ncbitaxonomist.model.datamodel


class Taxon(ncbitaxonomist.model.datamodel.DataModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__('taxon', attributes=attributes)
    attributes = ncbitaxonomist.model.datamodel.standardize_attributes(attributes)
    self.taxonid = ncbitaxonomist.model.datamodel.int_attribute(attributes.pop('taxid', None))
    self.parentid = ncbitaxonomist.model.datamodel.int_attribute(attributes.pop('parentid', None))
    self.rankname = attributes.pop('rank', None)
    self.names = attributes.pop('names', {})
    if self.rank == 'no rank' or self.rank is None:
      self.rank = ncbitaxonomist.utils.no_rank()

  def update_names(self, names:Mapping[str, str])->None:
    """Update taxon names from a dictionary with the structure {name:type}."""
    self.names.update(names)

  def update(self, taxon:Type[__qualname__])->None:
    """Update taxon names from another Taxon instance."""
    self.update_names(taxon.names)

  def get_attributes(self)->Dict[str,any]:
    """Return taxon attributes as dictionary. The scientific_name is injected to
    simplify parsing with other tools."""
    return {'taxid':self.taxonid, 'rank' : self.rankname, 'names':self.names,
            'parentid':self.parentid, 'name' : self.get_name_by_type()}

  def get_names(self)->Dict[str,str]:
    """Return names as dictionary with the structure name:type"""
    return self.names

  def get_name_by_type(self, nametype:str='scientific_name')->str:
    """Return specific name type if known."""
    for i in self.names:
      if self.names[i] == nametype:
        return i
    return None

  #def get_rank(self):
    #return self.rank

  def rank(self):
    return self.rankname

  #def get_parent(self)->int:
    #return self.parentid

  def add_parent(self, parentid):
    self.parentid = int(parentid)

  def isrank(self, rank):
    return self.rankname == rank

  def parent(self):
    return self.parentid
