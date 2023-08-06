"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json

import entrezpy.base.result
import entrezpy.log.logger


class NcbiMappingResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.mappings = {}
    self.logger = entrezpy.log.logger.get_class_logger(NcbiAccessionResult)
    self.logger.debug(json.dumps({'init':self.dump()}))

  def size(self):
    return len(self.mappings)

  def get_link_parameter(self, reqnum=0):
    del reqnum #Unused
    self.logger.warning(json.dumps({'Not supported':'Entrez links'}))

  def isEmpty(self):
    if not self.mappings:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'mapping': list(self.mappings)}

  def add_mapping(self, mapping):
    self.mappings.update(mapping)
