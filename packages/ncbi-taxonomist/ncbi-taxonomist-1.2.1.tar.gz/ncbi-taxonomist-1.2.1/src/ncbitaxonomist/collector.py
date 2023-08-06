"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Type

import ncbitaxonomist.analyzer.collect
import ncbitaxonomist.convert.ncbitaxon
import ncbitaxonomist.log.logger
import ncbitaxonomist.ncbitaxonomist
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.query.entrez
import ncbitaxonomist.query.collect.name
import ncbitaxonomist.query.collect.taxid


class Collector:
  """Implements remote collection of taxa from Entrez."""

  def __init__(self, taxonomist:Type[ncbitaxonomist.ncbitaxonomist.NcbiTaxonomist]):
    self.logger = ncbitaxonomist.log.logger.get_class_logger(Collector)
    self.cache = taxonomist.cache

  def collect(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
              names:Type[ncbitaxonomist.payload.name.NamePayload]):
    """Collect given names and/or taxids from Entrez"""
    if names.has_data():
      self.cache.cache_payload(self.collect_names(names, ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
      self.cache.cache_payload(names)

    if taxids.has_data():
      self.collect_taxids(taxids, ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter())
      self.cache.cache_payload(taxids)

    if taxids.has_data():
      self.logger.info(json.dumps({'collecting':{'failed':taxids.as_list()}}))
    if names.has_data():
      self.logger.info(json.dumps({'collecting':{'failed':taxids.as_list()}}))

  def collect_names(self, names:Type[ncbitaxonomist.payload.name.NamePayload],
                    converter:Type[ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter])->Type[ncbitaxonomist.payload.name.NamePayload]:
    """Collect names  from Entrez"""
    self.logger.debug(json.dumps({'Collecting':{'names':names.as_list()}}))
    ncq = ncbitaxonomist.query.collect.name.NameCollectQuery(names)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery()
    etq.query_names(names.as_list(), ncbitaxonomist.analyzer.collect.CollectAnalyzer(ncq, converter))
    return ncq.payload

  def collect_taxids(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
                     converter:Type[ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter])->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """Collect taxids  from Entrez"""
    self.logger.debug(json.dumps({'Collecting':{'taxids':taxids.as_list()}}))
    tcq = ncbitaxonomist.query.collect.taxid.TaxidCollectQuery(taxids)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery()
    etq.query_taxids(taxids.as_list(), ncbitaxonomist.analyzer.collect.CollectAnalyzer(tcq, converter))
    return tcq.payload
