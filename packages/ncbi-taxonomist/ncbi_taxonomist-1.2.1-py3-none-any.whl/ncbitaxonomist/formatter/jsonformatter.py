"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import io
import json
import os
import sys


import ncbitaxonomist.formatter.base

class JsonFormatter(ncbitaxonomist.formatter.base.BaseFormatter):

  def __init__(self):
    super().__init__(logcls=JsonFormatter)
    self.separators = (',', ':')

  def format_collection(self, model):
    self.write_stdout(model.get_attributes())

  def format_mapping(self, query, model, querycast):
    mapping = {'mode':'mapping', 'query':query, 'cast':model.cast}
    if model.cast == 'taxon':
      mapping.update({'taxon':model.get_attributes()})
    else:
      mapping.update({'accession':model.get_attributes()})
    self.write_stdout(mapping)

  def format_resolve(self, querycast, query, model, lineage):
    resolve = {'mode':'resolve', 'query':query, 'cast':model.cast}
    if querycast == 'accs':
      resolve.update({'accession':model.get_attributes()})
    else:
      resolve.update({model.cast:model.get_attributes()})
    resolve.update({'lineage':[x.get_attributes() for x in lineage]})
    self.write_stdout(resolve)

  def format_subtrees(self, lineages, taxid, name):
    subtrees = {'mode':'subtree'}
    query = taxid
    if name is not None:
      query = name
    subtrees.update({'query':query})
    for i in lineages:
      subtrees['subtree'] = [x.get_attributes() for x in i]
    self.write_stdout(subtrees)

  def write_stdout(self, data):
    sys.stdout.write(json.dumps(data, separators=self.separators)+'\n')
