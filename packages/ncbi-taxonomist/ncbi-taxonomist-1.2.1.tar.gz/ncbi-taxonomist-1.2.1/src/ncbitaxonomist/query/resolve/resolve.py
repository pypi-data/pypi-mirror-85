"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from __future__ import annotations
from typing import Type, Mapping, List, AbstractSet, Iterable


import ncbitaxonomist.model.taxon
import ncbitaxonomist.payload.payload
import ncbitaxonomist.resolve.lineageresolver
import ncbitaxonomist.utils


class ResolveQuery:

  @staticmethod
  def resolve_lineage(taxid:int, taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]])->List[Type[ncbitaxonomist.model.taxon.Taxon]]:
    return ncbitaxonomist.resolve.lineageresolver.resolve_lineage(taxid, taxa)

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload
    self.formatter = ncbitaxonomist.utils.get_formatter()

  def format_resolve_taxid(self, query, model, lineage):
    self.formatter.format_resolve('taxid', query, model, lineage)

  def format_resolve_name(self, query, model, lineage):
    self.formatter.format_resolve('name', query, model, lineage)

  def format_resolve_accession(self, query, model, lineage):
    self.formatter.format_resolve('accs', query, model, lineage)

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]]):
    raise NotImplementedError

