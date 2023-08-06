"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import sys
import json


import entrezpy.base.result
import entrezpy.log.logger


class NcbiTaxonomyResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.queries = set()
    self.taxa = {}
    self.logger = entrezpy.log.logger.get_class_logger(NcbiTaxonomyResult)
    self.logger.debug(json.dumps({'init':self.dump()}))

  def size(self):
    return len(self.queries)

  def get_link_parameter(self, reqnum=0):
    del reqnum #Unused
    self.logger.warning(json.dumps({'Not supported':'Entrez links'}))

  def isEmpty(self):
    if not self.queries:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size':self.size(), 'function':self.function,
            'queries':list(self.queries)}

  def add_queries(self, queries):
    self.queries |= queries

  def add_taxon(self, taxon):
    self.taxa.update({taxon.taxid(): taxon})
