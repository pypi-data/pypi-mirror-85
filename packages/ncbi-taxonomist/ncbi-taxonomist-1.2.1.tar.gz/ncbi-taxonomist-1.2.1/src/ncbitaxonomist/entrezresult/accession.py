"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json

import entrezpy.base.result
import entrezpy.log.logger


class NcbiAccessionResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request:object):
    super().__init__(request.eutil, request.query_id, request.db)
    self.accessions = {}
    self.logger = entrezpy.log.logger.get_class_logger(NcbiAccessionResult)
    self.logger.debug(json.dumps({'init':self.dump()}))

  def size(self):
    return len(self.accessions)

  def get_link_parameter(self, reqnum=0):
    del reqnum #Unused
    self.logger.warning(json.dumps({'Not supported':'Entrez links'}))

  def isEmpty(self):
    if not self.accessions:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'accs': list(self.accessions)}

  def add_accession(self, accs):
    self.accessions.update({accs.uid:accs})
