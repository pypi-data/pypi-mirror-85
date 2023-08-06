"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


import sys
import json
from typing import Dict, Iterable, List, Type

import ncbitaxonomist.cache.cache
import ncbitaxonomist.log.logger
import ncbitaxonomist.model.accession
import ncbitaxonomist.model.datamodel
import ncbitaxonomist.parser.stdout
import ncbitaxonomist.payload.payload
import ncbitaxonomist.payload.taxid


class AccessionMap(ncbitaxonomist.payload.payload.Payload):
  """
  Implements the special payload of an accession map. Because each taxid can
  have several accessions, data stores all accessions associated with a given
  taxid. accs stores the accessions instances. The results are stored in
  taxid_accs with taxids as key and a list of associated accs as value.
  """

  class Update(ncbitaxonomist.payload.payload.Payload.Update):

    def __init__(self, processed:bool=False, value:str=None):
      super().__init__(processed, value)

  def __init__(self):
    """
    Sets up payload and processes input data. If parse is False, do not read
    arguments or STDIN to allow different method.
    """
    super().__init__('accmap', args=None, parse=False)
    self.logger = ncbitaxonomist.log.logger.get_class_logger(AccessionMap)
    self.data:Dict[str,List[ncbitaxonomist.model.datamodel.DataModel]] = {}
    self.accs:Dict[str,Type[ncbitaxonomist.model.accession.Accession]] = {}
    self.taxid_accs:Dict[int,List[str]] = {}
    self.parse_stdin()

  def parse_args(self, args:Iterable[str]):
    """No arguments required. Is always parsed from STDIN."""
    pass

  def parse_stdin(self):
    self.logger.debug(json.dumps({'Parsing': 'STDIN'}))
    parser = ncbitaxonomist.parser.stdout.StdoutParser()
    for i in sys.stdin:
      attributes = parser.parse(i)
      if attributes['query'] is None or attributes['accession'] is None:
        sys.exit(self.logger.error(json.dumps({'missing values':attributes})))
      self.add_taxid_accs(attributes['accession'].get('taxid'), attributes.get('query'))
      self.add(attributes.pop('query'), attributes.pop('accession'))

  def add_taxid_accs(self, taxid:int, accession:str):
    if taxid is None:
      sys.exit(self.logger.error(json.dumps({'taxid cannot be None':taxid})))
    if int(taxid) not in self.taxid_accs:
      self.taxid_accs[int(taxid)] = []
    self.taxid_accs[int(taxid)].append(str(accession))

  def add(self, accession, attributes):
    if accession not in self.data:
      self.accs[accession] = ncbitaxonomist.model.accession.Accession(attributes)
      self.data[accession] = []

  def process(self, accession:str, result):
    """Checks if the accession model is part of the query"""
    if accession in self.data:
      self.data[accession] = result
      return AccessionMap.Update(True, accession)
    return AccessionMap.Update()

  def get_accession(self, acc:str):
    return self.accs.get(acc)

  def has_taxid(self, taxid:int)->bool:
    return taxid in self.taxid_accs

  def get_taxid_accsessions(self, taxid:int)->List[str]:
    return self.taxid_accs.get(int(taxid))

  def get_taxid_list(self)->List[int]:
    return list(self.taxid_accs)

  def get_data(self, datakey=None)->Dict:
    """Gets payload data."""
    if datakey is None:
      return self.data
    return self.data.get(str(datakey))

  def size(self)->int:
    """Gets the number of requested data."""
    if self.data is not None:
      return len(self.data)
    return 0

  def has_data(self)->bool:
    """Tests if payload contains any data."""
    if self.data is None or self.size() == 0:
      return False
    return True

  def as_list(self)->List[str]:
    """Returns data keys as list."""
    if self.data:
      return list(self.data)
    return []

  def is_processed(self, acc):
    """Tests if the accession has been processed."""
    if not self.data.get(str(acc)):
      return False
    return True

  def remove(self, acc):
    return self.data.pop(str(acc), None)

  def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
    """Accession lineages are not cached."""
    pass
