"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import sys
from typing import Dict, Type

import ncbitaxonomist.analyzer.accession
import ncbitaxonomist.analyzer.mapping
import ncbitaxonomist.convert.accessiondb
import ncbitaxonomist.convert.ncbiaccession
import ncbitaxonomist.convert.ncbitaxon
import ncbitaxonomist.convert.taxadb
import ncbitaxonomist.db.dbmanager
import ncbitaxonomist.log.logger
import ncbitaxonomist.ncbitaxonomist
import ncbitaxonomist.payload.accession
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.query.entrez
import ncbitaxonomist.query.map.accession
import ncbitaxonomist.query.map.name
import ncbitaxonomist.query.map.taxid


class Mapper:
  """Implements mapping commands for taxids, names, and accessions."""

  def __init__(self, taxonomist:Type[ncbitaxonomist.ncbitaxonomist.NcbiTaxonomist]):
    self.db = taxonomist.db
    self.cache = taxonomist.cache
    self.logger = ncbitaxonomist.log.logger.get_class_logger(Mapper)

  def map(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
          names:Type[ncbitaxonomist.payload.name.NamePayload],
          accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload],
          entrezdb:str, remote:bool=False):
    """
    Maps the passed payload. The mappign first checks names, followed by
    taxids and accessions. Because names will return the corresponding names and
    taxids, a query for names and taxids will arelady have fetched taxids which
    than can be faster solved via the cache. The caching of accessions is
    done in case a query contains several accessions refering to the same data.
    If a remote lookup is requested, such a query will be retrieved from cache.
    """
    if self.db is not None and names.has_data():
      self.cache.cache_payload(self.map_names(names))

    if self.db is not None and taxids.has_data():
      self.map_taxa_from_cache(taxids)
      if taxids.has_data():
        self.cache.cache_payload(self.map_taxids(taxids))

    if remote and names.has_data():
      self.map_taxa_from_cache(names)
      if names.has_data():
        self.cache.cache_payload(self.map_names_remote(names))

    if remote and taxids.has_data():
      self.map_taxa_from_cache(taxids)
      if taxids.has_data():
        self.cache.cache_payload(self.map_taxids_remote(taxids))

    if self.db and accessions.has_data():
      self.cache.cache_payload(self.map_accessions(accessions, entrezdb))

    if remote and accessions.has_data():
      self.map_taxa_from_cache(accessions)
      if accessions.has_data():
        self.cache.cache_payload(self.map_accessions_remote(accessions, entrezdb))

    if taxids.has_data():
      self.logger.info(json.dumps({'mapping':{'failed':taxids.as_list()}}))
    if names.has_data():
      self.logger.info(json.dumps({'mapping':{'failed':names.as_list()}}))
    if accessions.has_data():
      self.logger.info(json.dumps({'mapping':{'failed':accessions.as_list()}}))

  def map_names(self, names:Type[ncbitaxonomist.payload.name.NamePayload])->Type[ncbitaxonomist.payload.name.NamePayload]:
    """Maps name payloads locally."""
    self.logger.debug(json.dumps({'mapping':{names.cast:names.as_list(), 'db':self.db.path}}))
    nmq = ncbitaxonomist.query.map.name.NameMapQuery(names)
    self.db.get_taxa_by_name(names.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), nmq)
    return names

  def map_names_remote(self, names:Type[ncbitaxonomist.payload.name.NamePayload])->Type[ncbitaxonomist.payload.payload.Payload]:
    """Maps name payloads remotely."""
    self.logger.debug(json.dumps({'mapping':{names.cast:names.as_list(), 'db':'entrez::taxonomy'}}))
    nmq = ncbitaxonomist.query.map.name.NameMapQuery(names)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery()
    etq.query_names(names.as_list(),
                    ncbitaxonomist.analyzer.mapping.MapAnalyzer(nmq,
                                                                ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
    return names

  def map_taxids(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload])->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """Maps taxids payloads locally."""
    self.logger.debug(json.dumps({'mapping':{taxids.cast:taxids.as_list(), 'db':self.db.path}}))
    tmq = ncbitaxonomist.query.map.taxid.TaxidMapQuery(taxids)
    self.db.get_taxa_by_taxids(taxids.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), tmq)
    return taxids

  def map_taxids_remote(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload]
                        )->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """Maps taxids payloads remotely."""
    self.logger.debug(json.dumps({'mapping':{taxids.cast:taxids.as_list(), 'db':'entrez::taxonomy'}}))
    tmq = ncbitaxonomist.query.map.taxid.TaxidMapQuery(taxids)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery()
    etq.query_taxids(taxids.as_list(),
                     ncbitaxonomist.analyzer.mapping.MapAnalyzer(tmq,
                                                                 ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
    return taxids

  def map_accessions(self, accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload],
                     entrezdb:str)->Type[ncbitaxonomist.payload.accession.AccessionPayload]:
    """Maps accession payloads locally."""
    self.logger.debug(json.dumps({'mapping':{accessions.cast:accessions.as_list(), 'db':f'{self.db}::{entrezdb}'}}))
    amq = ncbitaxonomist.query.map.accession.AccessionMapQuery(accessions)
    self.db.get_taxa_by_accessions(accessions.as_list(),entrezdb,
                                   ncbitaxonomist.convert.accessiondb.DbAccessionConverter(),
                                   amq)
    return accessions

  def map_accessions_remote(self, accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload],
                            entrezdb:str)->Type[ncbitaxonomist.payload.accession.AccessionPayload]:
    """Maps accession payloads remotely."""
    self.logger.debug(json.dumps({'mapping':{accessions.cast:accessions.as_list(), 'db':f'entrez::{entrezdb}'}}))
    amq = ncbitaxonomist.query.map.accession.AccessionMapQuery(accessions)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery()
    etq.query_accessions(accessions.as_list(),
                         entrezdb,
                         ncbitaxonomist.analyzer.accession.AccessionMapAnalyzer(amq,
                                                                                ncbitaxonomist.convert.ncbiaccession.NcbiAccessionConverter()))
    return accessions

  def map_taxa_from_cache(self, pload:Type[ncbitaxonomist.payload.payload.Payload]):
    """
    Map queries from cache. Not the best loop but don't like to loop over
    different casts at once.

      .. note Unify cache retrieval. Along the lines of get_cache(cast).retrieve()
    """
    self.logger.debug(json.dumps({'mapping':pload.cast, 'db':'cache'}))
    if not pload.has_data():
      self.logger.debug(json.dumps({'payload':'empty'}))
      return
    if pload.cast == 'taxid':
      qry = ncbitaxonomist.query.map.taxid.TaxidMapQuery(pload)
      for i in pload.as_list():
        if self.cache.taxid_is_cached(i):
          qry.map_query(self.cache.get_taxon(i))
          if pload.is_processed(i):
            pload.remove(i)
    elif pload.cast == 'name':
      qry = ncbitaxonomist.query.map.name.NameMapQuery(pload)
      for i in pload.as_list():
        if self.cache.name_is_cached(i):
          qry.map_query(self.cache.get_taxon_by_name(i))
          if pload.is_processed(i):
            pload.remove(i)
    elif pload.cast == 'acc':
      qry = ncbitaxonomist.query.map.accession.AccessionMapQuery(pload)
      for i in pload.as_list():
        if self.cache.accession_is_cached(i):
          qry.map_query(self.cache.get_accession(i))
          if pload.is_processed(i):
            pload.remove(i)
    else:
      sys.exit("Unknown payload cast: {}.Abort".format(pload.cast))
