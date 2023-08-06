"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type, Mapping, AbstractSet, Iterable

import ncbitaxonomist.payload.payload
import ncbitaxonomist.model.taxon
import ncbitaxonomist.utils


class CollectQuery:

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload
    self.formatter = ncbitaxonomist.utils.get_formatter()

  def format(self, model):
    self.formatter.format_collection(model)

  def collect(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    raise NotImplementedError
