"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable, Type

import ncbitaxonomist.model.taxon
import ncbitaxonomist.query.collect.collect


class TaxidCollectQuery(ncbitaxonomist.query.collect.collect.CollectQuery):

  def collect(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    self.payload.process(taxon)
    self.format(taxon)
