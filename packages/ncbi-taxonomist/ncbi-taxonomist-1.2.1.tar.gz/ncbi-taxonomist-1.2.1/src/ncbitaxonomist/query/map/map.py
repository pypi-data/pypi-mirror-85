"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Type

import ncbitaxonomist.model.datamodel
import ncbitaxonomist.payload.payload
import ncbitaxonomist.utils


class MapQuery:

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload
    self.formatter = ncbitaxonomist.utils.get_formatter()

  def map_query(self, model:Type[ncbitaxonomist.model.datamodel.DataModel]):
    raise NotImplementedError

  def format_taxid_mapping(self, model):
    self.formatter.format_mapping(str(model.taxid()), model, 'taxid')

  def format_name_mapping(self, query, model):
    self.formatter.format_mapping(query, model, 'name')

  def format_accession_mapping(self, query, model):
    self.formatter.format_mapping(query, model, 'accession')
