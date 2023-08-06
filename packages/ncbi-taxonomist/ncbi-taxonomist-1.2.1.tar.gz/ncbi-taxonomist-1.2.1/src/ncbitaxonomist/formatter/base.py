"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import io
import json
import os
import sys

import ncbitaxonomist.log.logger

class BaseFormatter:

  def __init__(self, logcls=None):
    self.logger = ncbitaxonomist.log.logger.get_class_logger(BaseFormatter)
    if logcls is not None:
      self.logger = ncbitaxonomist.log.logger.get_class_logger(logcls)
    self.rootns = 'ncbitaxonomist'

  def format_resolve(self, querycast, query, model, lineage):
    raise NotImplementedError

  def format_collection(self, model):
    raise NotImplementedError

  def format_mapping(self, query, model, querycast):
    raise NotImplementedError

  def format_subtrees(self, lineages, taxid, name):
    raise NotImplementedError
