"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from __future__ import annotations
from typing import Dict, Iterable, Set, Type


import ncbitaxonomist.model.taxon


class TaxaCache:
  """
  Class to handle caching of taxa. Taxa are stored mapping taxid
  as key and  :class:`ncbitaxonomist.model.taxon.Taxon` instances as values.
  Names are stored mapping names as key and taxid as values.

  .. note:: Because Python used object reference, it could be more efficient
            to store the Taxon instance in the name dict as well.

  """

  def __init__(self):
    self.taxa:Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]] = {}
    self.names:Dict[str,int] = {}

  def cache(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    """Caches taxa and corresponding names"""
    if taxon.taxid() not in self.taxa:
      self.taxa[taxon.taxid()] = taxon
    for i in taxon.get_names():
      self.cache_name(i, taxon.taxid())

  def cache_name(self, name, taxid):
    """Caches names belonging to a taxid"""
    if name not in self.names:
      self.names[name] = taxid

  def get_taxa(self, taxids:Iterable[int]=None)->Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]]:
    """Returns given or all taxids in cache"""
    if taxids:
      taxa = {}
      for i in taxids:
        if i in self.taxa:
          taxa[i] = self.taxa[i]
      return taxa
    return self.taxa

  def get_taxon(self, taxid)->Type[ncbitaxonomist.model.taxon.Taxon]:
    """Returns given or all taxids in cache"""
    if taxid in self.taxa:
      return self.taxa[taxid]
    return None

  def names_to_taxids(self, names)->Set[int]:
    """Returns a taxid set for given names"""
    taxids = set()
    for i in names:
      if i in self.names:
        taxids.add(self.names[i])
    return taxids

  def incache(self, name=None, taxid=None)->bool:
    """Tests if a taxid or name is cached"""
    if taxid:
      return taxid in self.taxa
    return name in self.names

  def union(self, taxids, names)->Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]]:
    """Normalizes a taxid and name list by union"""
    union = {}
    for i in names:
      if i in self.names and self.names[i] in self.taxa:
        union[self.names[i]] = self.taxa[self.names[i]]
    for i in taxids:
      if (i not in union) and (i in self.taxa):
        union[i] = self.taxa[i]
    return union

  def is_empty(self):
    """Tests if cache is empty"""
    if self.taxa:
      return False
    return True
