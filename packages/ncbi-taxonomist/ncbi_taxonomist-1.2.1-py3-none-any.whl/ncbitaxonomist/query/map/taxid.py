"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type


import ncbitaxonomist.cache.cache
import ncbitaxonomist.model.taxon
import ncbitaxonomist.query.map.map


cache = ncbitaxonomist.cache.cache.Cache()

class TaxidMapQuery(ncbitaxonomist.query.map.map.MapQuery):
  """Implements a mapping query for taxonomy taxids."""

  def map_query(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    cache.cache_taxon(taxon)
    if self.payload.process(taxon).processed:
      self.format_taxid_mapping(taxon)
