"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import sys
from typing import Iterable, List, Type

import ncbitaxonomist.model.taxon
import ncbitaxonomist.payload.payload


class AccessionPayload(ncbitaxonomist.payload.payload.Payload):
  """
  Implements an accession payload for taxonomist queries using names.
  """

  class Update(ncbitaxonomist.payload.payload.Payload.Update):

    def __init__(self, processed:bool=False, value:str=None):
      super().__init__(processed, value)

  def __init__(self, args:Iterable[str]=None, parse:bool=True):
    super().__init__('acc', args, parse)

  def parse_args(self, args:Iterable[str]):
    """Parses expected name arguments"""
    while args:
      for i in filter(bool, [x.strip() for x in args.pop().split(',') if x]):
        self.data[str(i)] = []

  def parse_stdin(self):
    """Reads standard input expecting names"""
    for i in sys.stdin:
      for j in filter(bool, [x.strip() for x in i.strip().split(',') if x]):
        self.data[str(j)] = []

  def process(self, model:Type[ncbitaxonomist.model.accession.Accession], result:List=None):
    """ToDo: change order key/values in accession dict."""
    #if str(model.uid) in self.data:
      #self.data[model.uid] = model
      #return AccessionPayload.Update(True, model.uid)
    for i in model.get_accessions().values():
      if i in self.data and result is not None:
        self.data[i] += result
        return AccessionPayload.Update(True, i)
      if i in self.data:
        self.data[i].append(model)
        return AccessionPayload.Update(True, i)
    return AccessionPayload.Update()

  def as_list(self)->List[str]:
    """Gets the requested accessions as list."""
    return list(self.data)

  def is_processed(self, acc):
    """Tests if the accession has been processed."""
    if not self.data.get(str(acc)):
      return False
    return True

  def remove(self, acc):
    """Removes accession from payload."""
    return self.data.pop(str(acc), None)

  def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
    if cache.accession.is_empty():
      return
    for i in self.as_list():
      if cache.accession.incache(i):
        self.data.pop(i)

  def get_data(self, datakey=None):
    if datakey is None:
      return self.data
    return self.data.get(str(datakey))
