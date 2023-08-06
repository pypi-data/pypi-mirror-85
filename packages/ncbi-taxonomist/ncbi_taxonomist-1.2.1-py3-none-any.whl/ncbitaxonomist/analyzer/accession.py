"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from __future__ import annotations

import os
import sys
import json
import http.client
from typing import Type

import entrezpy.base.analyzer
import entrezpy.log.logger

import ncbitaxonomist.query.map.map
import ncbitaxonomist.entrezresult.accession
import ncbitaxonomist.convert.ncbiaccession


class AccessionMapAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  Implements an entrezpy analyzer to parse accession mappings from NCBI.
  """
  def __init__(self, query:Type[ncbitaxonomist.query.map.map.MapQuery],
               converter:Type[ncbitaxonomist.convert.ncbiaccession.NcbiAccessionConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.isFatalError = None
    self.logger = entrezpy.log.logger.get_class_logger(AccessionMapAnalyzer)

  def init_result(self, response:dict, request:object) -> bool:
    if not self.result:
      self.result = ncbitaxonomist.entrezresult.accession.NcbiAccessionResult(request)
      return True
    return False

  def analyze_error(self, response:dict, request:object):
    if 'invalid uid' in response['error'].lower():
      self.logger.warning(json.dumps({'Bad uid(s)':response['error']}))
      self.isFatalError = False
    else:
      self.logger.error(json.dumps({'response-Error':{
                                    'request-dump' : request.dump_internals(),
                                    'error' : response}}))
      self.isFatalError = True
      self.hasErrorResponse = True

  def analyze_result(self, response:dict, request:object):
    self.init_result(request, request)
    uids = response['result'].pop('uids', None)
    if uids:
      for i in uids:
        model = self.converter.convert_to_model(response['result'].pop(i), request.db)
        if model:
          self.result.add_accession(model)
          self.query.map_query(model)

  def parse(self, raw_response:Type[http.client.HTTPResponse], request:Type[entrezpy.base.request.EutilsRequest]):
    """
    Check for errors and calls parser for the raw response. Implements the
    :meth:`entrezpy.base.analyzer.EutilsAnalyzer.parse`.
    """
    if request.retmode not in entrezpy.base.analyzer.EutilsAnalyzer.known_fmts:
      self.logger.error(json.dumps({'unknown format': request.retmode}))
    response = self.convert_response(raw_response.read().decode('utf-8'), request)
    if self.isErrorResponse(response, request):
      self.analyze_error(response, request)
    if not self.isFatalError:
      self.analyze_result(response, request)
    if self.result is None:
      sys.exit(json.dumps({'result attribute': 'not set', 'action' : 'abort'}))
