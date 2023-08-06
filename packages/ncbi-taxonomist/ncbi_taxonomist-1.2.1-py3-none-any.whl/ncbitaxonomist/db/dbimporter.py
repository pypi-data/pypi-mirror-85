"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
from typing import Dict, Iterable, Mapping, Type

import ncbitaxonomist.config
import ncbitaxonomist.db.dbmanager
import ncbitaxonomist.log.logger


logger = ncbitaxonomist.log.logger.get_logger(__name__)

def parse_taxa(data:Mapping[str,any], taxa:Iterable, names:Iterable):
  """Parse taxa data from STDIN"""
  taxid = data.pop('taxid')
  taxa.append((taxid, data.pop('rank'), data.pop('parentid')))
  if 'names' in data:
    for i in data['names']:
      names.append((taxid, i, data['names'][i]))

def commit(db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb], taxa:Iterable[tuple],
           names:Iterable[tuple], accessions:Iterable[tuple]=None,
           taxids:Iterable[tuple]=None):
  """Commit data into local database. Order of commits is important."""
  if taxa:
    logger.debug(json.dumps({'db':db.path, 'op':'commit',  'taxa':f'{len(taxa)}', 'names':f'{len(names)}'}))
    db.add_taxa(taxa)
    db.add_names(names)
    taxa = []
    names = []
  if accessions:
    logger.debug(json.dumps({'db':db.path, 'op':'commit',  'accs':f'{len(accessions)}', 'taxid':f'{len(taxids)}'}))
    db.add_taxids(taxids)
    db.add_accessions(accessions)
    accessions = []
    taxids = []

def parse_taxa_list(taxalist, taxa, names):
  if taxalist is None:
    sys.exit("Missing expected taxalist. Abort")
  for i in taxalist:
    parse_taxa(i, taxa, names)

def parse_accession(data:Mapping[str,any], accessions:Iterable, taxids:Iterable,
                    taxa:Iterable, names:Iterable):
  """Parse accessions data from STDIN"""
  taxid = data.pop('taxid')
  db = data.pop('db')
  uid = data.pop('uid')
  for i in data['accessions']:
    accessions.append((data['accessions'][i], i, db, uid, taxid))
  if 'lineage' in data:
    parse_lineage(data['lineage'], taxa, names)
  taxids.append((taxid,))

def import_stdin(db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb], out_attrib:str=None):
  """Parse JSON STDIN and add data to local database"""
  batch_size = 100000
  taxa = []
  names = []
  taxids = []
  accessions = []
  logger.debug(json.dumps({'db':db.path, 'op':'parsing STDIN'}))
  for i in sys.stdin:
    #attribs = filter_attribute(i, out_attrib)
    linein = json.loads(i.strip())
    mode = linein.get('mode')
    if mode is None:
      parse_taxa(linein, taxa, names)
    else:
      if mode == 'resolve':
        parse_taxa_list(linein.get('lineage'), taxa, names)
      elif mode == 'mapping' and linein.get('accession') is not None:
        parse_accession(linein['accession'], accessions, taxids, taxa, names)
        if len(accessions) % batch_size == 0:
          commit(db, taxa, names, accessions, taxids)
      elif mode == 'mapping' and linein.get('taxon') is not None:
        parse_taxa(linein.get('taxon'), taxa, names)
      elif mode == 'subtree':
        for j in linein['subtrees']:
          parse_taxa_list(linein['subtrees'][j], taxa, names)
      else:
        sys.exit(logger.error(json.dumps({'unknown mode': mode})))
    if len(taxa) % batch_size == 0:
      commit(db, taxa, names)
    sys.stdout.write(i)
  if taxa:
    commit(db, taxa, names)
  if accessions:
    commit(db, taxa, names, accessions, taxids)
