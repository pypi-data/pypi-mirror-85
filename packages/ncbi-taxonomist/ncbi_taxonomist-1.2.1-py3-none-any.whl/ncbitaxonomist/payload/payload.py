"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

from typing import Dict, Iterable, List, Type

import ncbitaxonomist.cache.cache
import ncbitaxonomist.model.datamodel


class Payload:
  """
  Implements the basic payload for a taxonomist query to parse the input data
  and to keep track of requested data. Data can be taxids, names, and
  accessions, corresponding to two types. Payloads should enforce the proper
  type of input data throughout a taxonomist command. Data can be parsed from
  an argument list, STDIN, or implemented specifically. To avoid waiting for
  STDIN when implementing a specific parser, parsing can be deactivated upon
  initialization.
  """

  class Update:
    """
    Stores the processing result of a single input data.
    """

    def __init__(self, processed:bool=False, value=None):
      self.processed = processed
      self.value = value

  def __init__(self, cast:str, args:Iterable[str]=None, parse:bool=True):
    """Sets up payload and processes input data. If parse is False, do not
    read arguments or STDIN to allow different method."""
    self.cast = cast
    self.data:Dict[str,List[Type[ncbitaxonomist.model.datamodel.DataModel]]] = {}
    if parse:
      self.parse(args)

  def parse(self, args:Iterable[str]=None):
    """Checks if reading STDIN or arguments."""
    if args is not None and not args: #empty args list
      self.parse_stdin()
    if args:
      self.parse_args(args)

  def parse_args(self, args:Iterable[str]):
    """Virtual function to implement the corresponding argument parsing."""
    raise NotImplementedError

  def parse_stdin(self):
    """Virtual function to implement the corresponding STDIN parsing."""
    raise NotImplementedError

  def process(self, model:Type[ncbitaxonomist.model.datamodel.DataModel]):
    """Virtual function to process data from requests and keep track of
    data which has not been processed by the requested command, i.e. found,
    fetched, resolved, etc"""
    raise NotImplementedError

  def get_data(self, datakey=None)->Dict:
    """Gets payload data."""
    raise NotImplementedError

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

  #def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
  def update_from_cache(self, cache):
    """Update payload from cache by removing already cached data."""
    raise NotImplementedError
