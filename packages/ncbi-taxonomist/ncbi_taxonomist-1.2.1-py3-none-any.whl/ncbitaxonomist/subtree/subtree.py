"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from __future__ import annotations
from typing import Type
import ncbitaxonomist.model.taxon

class Subtree:
  """
  Implements subtree and collects children taxids in addition to taxa.
  """

  class Node:
    """
    Stores taxid and its children.
    """
    def __init__(self, taxid:int, parentid:int=None):
      self.taxid = taxid
      self.parentid = parentid
      self.children = set()

  def __init__(self):
    self.taxa = {}
    self.nodes = {}

  def add_taxon(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    """Adds taxa to subtree"""
    if taxon.taxid() not in self.taxa:
      self.taxa[taxon.taxid()] = taxon
    if taxon.taxid() not in self.nodes:
      self.nodes[taxon.taxid()] = Subtree.Node(taxon.taxid())
    if taxon.parent() is not None and taxon.parent() not in self.nodes:
      self.nodes[taxon.parent()] = Subtree.Node(taxon.parent())
    self.nodes[taxon.taxid()].parentid = taxon.parent()
    if taxon.parent() is not None:
      self.nodes[taxon.parent()].children.add(taxon.taxid())

  def isCollected(self, taxid:int)->bool:
    """Tests is taxa is collected. Should be replaces by meth:`has_taxon`."""
    return taxid in self.taxa

  def has_taxon(self, taxid:int):
    """Tests is taxa is collected. """
    return taxid in self.taxa

  def get_taxon(self, taxid:int):
    """Getter for a taxon."""
    return self.taxa[taxid]
