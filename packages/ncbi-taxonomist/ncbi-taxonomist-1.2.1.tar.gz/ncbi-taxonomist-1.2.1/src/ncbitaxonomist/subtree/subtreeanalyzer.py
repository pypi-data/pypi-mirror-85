"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
from typing import Type, Iterable, List

import ncbitaxonomist.convert.taxadb
import ncbitaxonomist.db.dbmanager
import ncbitaxonomist.log.logger
import ncbitaxonomist.model.taxon
import ncbitaxonomist.resolve.lineageresolver
import ncbitaxonomist.subtree.subtree
import ncbitaxonomist.utils


class SubtreeAnalyzer:
  """Extracts requested ranks deom collected subtrees."""
  def __init__(self, db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb]):
    self.logger = ncbitaxonomist.log.logger.get_class_logger(SubtreeAnalyzer)
    self.db = db
    self.formatter = ncbitaxonomist.utils.get_formatter()

  def subtree(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
              names:Type[ncbitaxonomist.payload.name.NamePayload], rank:str=None,
                  upper_rank:str=None, lower_rank:str=None, remote:bool=False):
    """
    Organizes ranks, collects subtrees and runs the rank clipping.
    """

    if upper_rank is not None or lower_rank is not None:
      if upper_rank == lower_rank:
        rank = upper_rank
      else:
        rank = None
    if rank is not None:
      upper_rank = None
      lower_rank = None
    self.logger.debug(json.dumps({'subtree-rank':rank, 'subtree-from':lower_rank,
                                  'subtree-to':upper_rank}))
    if self.db: #ToDo: fetch by rank
      stree = self.get_subtree(taxids.as_list(), names.as_list())
      if taxids.has_data():
        for i in taxids.as_list():
          if stree.has_taxon(i):
            self.assemble_lineage(i, stree, rank, upper_rank, lower_rank)
          else:
            self.logger.info(json.dumps({'taxid not in database': i}))
      if names.has_data():
        mapping = self.db.names_to_taxid(names.as_list())
        for i in names.as_list():
          if i in mapping:
            self.assemble_lineage(mapping[i], stree, rank, upper_rank, lower_rank, i)
          else:
            self.logger.info(json.dumps({'name not in database': i}))

  def get_subtree(self, taxids:Iterable[int], names:Iterable[int])->Type[ncbitaxonomist.subtree.subtree.Subtree]:
    """Collects subtree for given taxon ids. """
    subtree = ncbitaxonomist.subtree.subtree.Subtree()
    if names:
      for i in self.db.get_taxa_by_name(names, ncbitaxonomist.convert.taxadb.TaxaDbConverter()):
        self.db.collect_subtree(i, ncbitaxonomist.convert.taxadb.TaxaDbConverter(), subtree)
    if taxids:
      for i in taxids:
        self.db.collect_subtree(i, ncbitaxonomist.convert.taxadb.TaxaDbConverter(), subtree)
    return subtree

  def assemble_lineage(self, taxid, subtree, rank, upper_rank, lower_rank, name=None)->List[List[Type[ncbitaxonomist.model.taxon.Taxon]]]:
    """
    Assemble the linage for a given taxid. If a name is given, use it
    in the result instead of the taxid.
    """
    lineages = []
    paths = self.backtrack(subtree.taxa, subtree.nodes, subtree.nodes[taxid],
                           self.set_rank_cutoff(rank, lower_rank), [], set())
    for i in paths:
      clipped = self.clip_ranks(subtree, i, rank, upper_rank, lower_rank)
      if clipped:
        if rank and self.test_single(clipped, rank):
          lineages.append(clipped)
        elif upper_rank and lower_rank:
          if (self.test_rank(clipped[-1], upper_rank) and
              self.test_rank(clipped[0], lower_rank)):
            lineages.append(clipped)
        elif upper_rank  and self.test_rank(clipped[-1], upper_rank):
          lineages.append(clipped)
        elif lower_rank and self.test_rank(clipped[0], lower_rank):
          lineages.append(clipped)
        else:
          if rank is None and upper_rank is None and lower_rank is None:
            lineages.append(clipped)
    if lineages:
      self.formatter.format_subtrees(lineages, taxid, name)
    else:
      self.logger.info(json.dumps({'no subtree for taxid': taxid}))
  def test_single(self, path, rank)->bool:
    """Tests if the result is a single rank and rquested rank."""
    if (len(path) != 1) or not path[0].isrank(rank):
      return False
    return True

  def test_rank(self, taxon, rank)->bool:
    """Tests it the taxon is the requested rank"""
    if not taxon.isrank(rank):
      return False
    return True

  def clip_ranks(self, subtree, path, rank, upper_rank, lower_rank):
    """Remove not requested ranks"""
    if upper_rank is not None and lower_rank is not None:  # taxa between upper and lower rank for given taxid
      if (path[0].rank() == upper_rank) and (path[-1].rank() == lower_rank):
        return path
    if path[0].parent() is not None:
      self.db.get_taxid_lineage(
        path[0].parent(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(),
        taxa=subtree.taxa)
    return ncbitaxonomist.resolve.lineageresolver.resolve_lineage(
      path[-1].taxid(), subtree.taxa, start=lower_rank, stop=upper_rank,
      single=rank)

  def set_rank_cutoff(self, rank, lower_rank):
    """Set lowest rank to look for. If none is given, find lowest, i.e. rank
       without children"""
    if rank is not None:
      return rank
    if lower_rank is not None:
      return lower_rank
    return None

  def backtrack(self, taxa, nodes, node, rank_cutoff, path, visited)->List[List]:
    """Find all lineages above starting node."""
    path = path + [taxa[node.taxid]]
    visited.add(node.taxid)
    if self.return_path(taxa, node, rank_cutoff):
      return [path]
    paths = []
    for i in node.children:
      if i not in visited:
        paths += self.backtrack(taxa, nodes, nodes[i], rank_cutoff, path, visited)
    return paths

  def return_path(self, taxa, node, rank_cutoff):
    """Tests if we can break backtracking. The boolean test could be likely
       inverted but has clearer conditions."""
    if(((rank_cutoff is None) and (not node.children)) or not node.children or
        (rank_cutoff and taxa[node.taxid].rank == rank_cutoff)):
      return True
    return False
