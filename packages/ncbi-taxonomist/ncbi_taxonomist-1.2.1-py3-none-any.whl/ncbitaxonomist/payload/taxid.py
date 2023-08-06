"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


import sys
from typing import Iterable, List, Type

import ncbitaxonomist.payload.payload
import ncbitaxonomist.model.taxon

class TaxidPayload(ncbitaxonomist.payload.payload.Payload):
  """
  Implements a taxid payload for taxonomist queries using taxids.
  """

  class Update(ncbitaxonomist.payload.payload.Payload.Update):

    def __init__(self, processed:bool=False, value:int=None):
      super().__init__(processed, value)

  def __init__(self, args:Iterable[str]=None, parse:bool=True):
    super().__init__('taxid', args)

  def parse_args(self, args:Iterable[str]):
    while args:
      for  i in filter(bool, [x for x in args.pop().split(',') if x]):
        self.data[int(i)] = []

  def parse_stdin(self):
    for i in sys.stdin:
      for j in filter(bool, [x.strip() for x in i.strip().split(',') if x]):
        self.data[int(j)] = []

  def add(self, taxid):
    self.data[int(taxid)] = []

  def process(self, model:Type[ncbitaxonomist.model.taxon.Taxon], result:List=None):
    if model.taxid() in self.data and result is not None and result:
      self.data[model.taxid()] += result
      return TaxidPayload.Update(True, model.taxid())
    if model.taxid() in self.data and result is None:
      self.data[model.taxid()].append(model)
      return TaxidPayload.Update(True, model.taxid())
    return TaxidPayload.Update()

  def as_list(self)->List[int]:
    """Gets the taxids  as list."""
    if self.data:
      return list(self.data)
    return []

  def get_data(self, datakey=None)->List[Type[ncbitaxonomist.model.datamodel.DataModel]]:
    if datakey is None:
      return self.data
    return self.data.get(int(datakey))

  def is_processed(self, taxid)->bool:
    """Tests if the taxid has been processed."""
    if not self.data.get(int(taxid)):
      return False
    return True

  def remove(self, taxid)->List[Type[ncbitaxonomist.model.datamodel.DataModel]]:
    """Removes taxid from payload."""
    return self.data.pop(int(taxid), None)

  def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
    if self.size() == 0:
      return
    if cache.taxa.is_empty():
      return
    for i in self.as_list():
      if cache.taxa.incache(taxid=i):
        self.data.pop(i)

  def contains(self, taxid:int)->bool:
    return taxid in self.data
