"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import AbstractSet, List, Mapping, Type

import ncbitaxonomist.model.accession
import ncbitaxonomist.model.taxon
import ncbitaxonomist.resolve.lineageresolver


cache = ncbitaxonomist.cache.cache.Cache()

class AccessionResolveQuery(ncbitaxonomist.query.resolve.resolve.ResolveQuery):

  def update_queries(self, acc):
    if acc not in self.accs:
      self.accs[acc] = None
    return self.accs[acc]

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]]):
    for i in taxids:
      taxon = taxa.get(i)
      if taxon:
        cache.cache_taxon(taxon)
        if i in self.payload.taxid_accs:
          for j in self.payload.taxid_accs[i]:
            if self.payload.process(j, AccessionResolveQuery.resolve_lineage(i, taxa)).processed:
              self.format_resolve_name(j,
                                       self.payload.get_accession(j),
                                       [x for x in self.payload.get_data(j)])
