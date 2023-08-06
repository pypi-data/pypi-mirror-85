"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from __future__ import annotations

import json
from typing import Dict, Iterable, List, Mapping, Type

import ncbitaxonomist.model.taxon
import ncbitaxonomist.log.logger


logger = ncbitaxonomist.log.logger.get_logger(__name__)

def find_taxon(taxid, taxa):
  if taxid in taxa:
    return taxa[taxid]
  return None

def assemble_lineage(taxid, taxa, start, stop, single):
  """Assemble lineage from leaf/start rank to root/stop rank"""
  taxon = find_taxon(taxid, taxa)
  if not taxon:
    return None
  collect = set_collect_flag(start, single)
  logger.debug("assemble lin:start:{}>stop>{}>single{}".format(start, stop, single))
  lineage = []
  while taxon.parent() is not None:
    logger.debug(f"current taxon:{taxon.get_attributes()}, start:{start}, stop: {stop}")
    if single is not None and taxon.isrank(single):
      lineage.append(taxon)
      logger.debug("add single {}".format(taxon.get_attributes()))
      return lineage
    if start is not None and taxon.isrank(start):
      logger.debug("start asm: {}".format(taxon.get_attributes()))
      collect = True
    if stop is not None and taxon.isrank(stop):
      logger.debug("stop asm: {}".format(taxon.get_attributes()))
      lineage.append(taxon)
      return lineage
    if collect:
      logger.debug("asm: {}".format(taxon.get_attributes()))
      lineage.append(taxon)
    taxon = find_taxon(taxon.parent(), taxa)
    if taxon is None:
      return []

  if start is not None and taxon.isrank(start):
    logger.debug("last start: add single {}".format(single))
    lineage.append(taxon)
  elif stop is not None and taxon.isrank(stop):
    logger.debug("last stop: add {}".format(single))
    lineage.append(taxon)
  else:
    logger.debug("last: add {}".format(single))
    lineage.append(taxon)
  return lineage

def set_collect_flag(start, single):
  """Set collection flag based on requested ranks"""
  if single is not None:
    return False
  if start is not None:
    return False
  return True

def resolve_lineages(taxids:Iterable[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]],
                     start=None, stop=None, single=None)->Dict[int,List[Type[ncbitaxonomist.model.taxon.Taxon]]]:
  """Resolve lineage for given taxids in given taxa"""
  lineages:Dict[int,List[Type[ncbitaxonomist.model.taxon.Taxon]]] = {}
  for i in taxids:
    lineages[i] = resolve_lineage(i, taxa, start, stop, single)
  return lineages

def resolve_lineage(taxid:int, taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]],
                    start=None, stop=None, single=None)->List[Type[ncbitaxonomist.model.taxon.Taxon]]:
  """Resolve lineage for given taxid in given taxa"""
  return assemble_lineage(taxid, taxa, start, stop, single)
