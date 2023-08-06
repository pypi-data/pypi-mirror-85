"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from __future__ import annotations
import sys
from typing import Dict, Iterable, List, Set, Type


import ncbitaxonomist.model.taxon
import ncbitaxonomist.model.accession
import ncbitaxonomist.payload.payload
import ncbitaxonomist.cache.taxa
import ncbitaxonomist.cache.accession


class Cache:
  """
  Handle caching of taxa, accessions and lineages. Taxa are stored as
  :class:`ncbitaxonomist.model.taxon.Taxon`. Lineages and accessions
  are stored referencing the corresponding taxid in the Taxa cache.
  """

  taxa = ncbitaxonomist.cache.taxa.TaxaCache()
  accessions = ncbitaxonomist.cache.accession.AccessionCache()

  def __init__(self):
    pass

  def cache_lineage(self, lin):
    """Caches lineages"""
    if lin:
      for i in lin:
        Cache.taxa.cache(i)

  def names_to_taxids(self, names)->Set[int]:
    """Converts names to corresponding taxids."""
    if not names:
      return set()
    return Cache.taxa.names_to_taxids(names)

  def get_taxa(self, taxids:Iterable[int]=None)->Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]]:
    """Retrieve given or all taxa form taxa cache."""
    return Cache.taxa.get_taxa(taxids)

  def get_taxon(self, taxid:int)->Type[ncbitaxonomist.model.taxon.Taxon]:
    """Retrieve given or all taxa form taxa cache."""
    return Cache.taxa.get_taxon(taxid)

  def get_taxon_by_name(self, name:str)->Type[ncbitaxonomist.model.taxon.Taxon]:
    """Retrieve given or all taxa form taxa cache."""
    if Cache.taxa.incache(name=name):
      return Cache.taxa.taxa[Cache.taxa.names[name]]
    return None

  def get_taxon_by_accession(self, accession:str)->Type[ncbitaxonomist.model.taxon.Taxon]:
    """Retrieve given or all taxa form taxa cache."""
    if  Cache.accessions.incache(accession):
      return Cache.taxa.taxa[Cache.accessions.accessions[accession]]
    return None

  def taxid_is_cached(self, taxid:int)->bool:
    """Tests if a taxon is cached using its taxid."""
    return Cache.taxa.incache(taxid=taxid)

  def name_is_cached(self, name:str)->bool:
    """Test if a taxon is cached using its taxid."""
    return Cache.taxa.incache(name=name)

  def accession_is_cached(self, name:str)->bool:
    """Test if a taxon is cached using its taxid."""
    return Cache.accessions.incache(name=name)

  def union_taxid_names(self, taxids:Iterable[int], names:Iterable[str])->Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]]:
    """Standardize names and taxids into a taxid:class:`taxon.Taxon` dict."""
    if taxids is None:
      taxids = []
    if names is None:
      names = []
    return Cache.taxa.union(taxids, names)

  def cache_taxon(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    """Cache taxon"""
    Cache.taxa.cache(taxon)

  def cache_taxa(self, taxa:List[Type[ncbitaxonomist.model.taxon.Taxon]]):
    """Cache taxa"""
    for i in taxa:
      Cache.taxa.cache(i)

  def cache_accession(self, acc:Type[ncbitaxonomist.model.accession.Accession]):
    """Cache accession"""
    Cache.accessions.cache(acc)

  def cache_accessions(self, accs:List[Type[ncbitaxonomist.model.accession.Accession]]):
    """Cache accession"""
    for i in accs:
      Cache.accessions.cache(i)

  def get_accession(self, acc:str)->Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]]:
    """Retrieve given or all taxa form taxa cache."""
    return Cache.accessions.get_accession(acc)

  def cache_payload(self, pload):
    """Remove and cache obtained data from payload."""
    for i in pload.as_list():
      if pload.is_processed(i):
        if pload.cast == 'taxid':
          self.cache_taxa(pload.remove(i))
        elif pload.cast == 'name':
          self.cache_taxa(pload.remove(i))
        elif pload.cast == 'acc':
          self.cache_accessions(pload.remove(i))
        elif pload.cast == 'accmap':
          pload.remove(i)
        else:
          sys.exit("Error. Invalid cache name {}. Abort".format(pload.cast))
