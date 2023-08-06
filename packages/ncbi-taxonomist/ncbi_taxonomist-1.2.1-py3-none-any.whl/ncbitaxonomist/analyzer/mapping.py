"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import os
import sys
import json
from typing import Type

import entrezpy.base.analyzer
import entrezpy.log.logger

import ncbitaxonomist.parser.ncbi.taxonomy
import ncbitaxonomist.convert.ncbitaxon
import ncbitaxonomist.entrezresult.taxonomy
import ncbitaxonomist.query.map.map


class MapAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  Implements an entrezpy analyzer to parse taxonomy XML data from NCBI and runs
  the obtained taxa through a map query.
  """
  taxa = {}

  def __init__(self, query:Type[ncbitaxonomist.query.map.map.MapQuery],
               converter:Type[ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.taxonomy_parser = ncbitaxonomist.parser.ncbi.taxonomy.TaxoXmlParser(MapAnalyzer.taxa)
    self.logger = entrezpy.log.logger.get_class_logger(MapAnalyzer)

  def init_result(self, response, request:object) -> bool:
    if not self.result:
      self.result = ncbitaxonomist.entrezresult.taxonomy.NcbiTaxonomyResult(request)
      return True
    return False

  def analyze_error(self, response, request:object):
    self.logger.error(json.dumps({'response':{'request-dump':request.dump_internals(),
                                              'error':response.getvalue()}}))

  def analyze_result(self, response, request:object):
    self.init_result(response, request)
    results = self.taxonomy_parser.parse(response)
    self.result.add_queries(results.queries)
    for i in results.taxa:
      m = self.converter.convert_to_model(results.taxa[i].attribute_dict())
      self.query.map_query(m)
