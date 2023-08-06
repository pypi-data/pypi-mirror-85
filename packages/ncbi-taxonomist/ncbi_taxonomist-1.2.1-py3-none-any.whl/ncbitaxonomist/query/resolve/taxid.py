"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable, List, Mapping, Type

import ncbitaxonomist.cache.cache
import ncbitaxonomist.model.taxon
import ncbitaxonomist.query.resolve.resolve


cache = ncbitaxonomist.cache.cache.Cache()

class TaxidResolveQuery(ncbitaxonomist.query.resolve.resolve.ResolveQuery):

  def resolve(self, taxids:List[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]]):
    for i in taxids:
      taxon = taxa.get(i)
      if taxon:
        cache.cache_taxon(taxon)
        update = self.payload.process(taxon, TaxidResolveQuery.resolve_lineage(i, taxa))
        if update.processed:
          self.format_resolve_taxid(str(update.value), taxon, [x for x in self.payload.get_data(update.value)])
