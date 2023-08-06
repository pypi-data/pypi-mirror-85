"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Iterable, Type

import ncbitaxonomist.cache.cache
import ncbitaxonomist.model.accession
import ncbitaxonomist.query.map.map


cache = ncbitaxonomist.cache.cache.Cache()

class AccessionMapQuery(ncbitaxonomist.query.map.map.MapQuery):

  def map_query(self, acc:Type[ncbitaxonomist.model.accession.Accession]):
    cache.cache_accession(acc)
    update = self.payload.process(acc)
    if update.processed:
      self.format_accession_mapping(update.value, acc)
