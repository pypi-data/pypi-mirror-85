"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from __future__ import annotations
import json
import sqlite3
from typing import Iterable, Dict, List, Mapping, Tuple, Type


import ncbitaxonomist.convert.converter
import ncbitaxonomist.convert.taxadb
import ncbitaxonomist.db.table.accessions
import ncbitaxonomist.db.table.groups
import ncbitaxonomist.db.table.names
import ncbitaxonomist.db.table.taxa
import ncbitaxonomist.log.logger
import ncbitaxonomist.model.datamodel
import ncbitaxonomist.query.map.map
import ncbitaxonomist.query.resolve.resolve
import ncbitaxonomist.subtree.subtree


class TaxonomyDb:
  """
  Implements the taxonomist database. It manages all operation to add, modify,
  and retrieve taxonomic data.
  """

  def __init__(self, dbpath:str, verbosity:int=0):
    self.path = dbpath
    self.connection = self.init_connection()
    self.taxa = ncbitaxonomist.db.table.taxa.TaxaTable(self.path).create(self.connection)
    self.names = ncbitaxonomist.db.table.names.NameTable(self.path).create(self.connection)
    self.accs = ncbitaxonomist.db.table.accessions.AccessionTable(self.path).create(self.connection)
    self.groups = ncbitaxonomist.db.table.groups.GroupTable(self.path).create(self.connection)
    self.logger = ncbitaxonomist.log.logger.get_class_logger(TaxonomyDb)
    self.logger.debug(json.dumps({'init':{'path':self.path,
                                  'tables':{'taxa':self.taxa.name,
                                            'names':self.names.name,
                                            'accessions':self.accs.name,
                                            'groups':self.groups.name}}}))

  def init_connection(self)->sqlite3.Connection:
    """Setup connection to local database"""
    connection = sqlite3.connect(self.path)
    connection.execute("PRAGMA foreign_keys=1")
    connection.row_factory = sqlite3.Row
    return connection

  def connect(self) -> sqlite3.Connection:
    """Connect to local database"""
    if self.connection is None:
      return self.init_connection(self.path)
    return self.connection

  def close_connection(self)->None:
    """Close connection to local database"""
    self.logger.debug(json.dumps({'closing':{'connection':self.connection,
                                             'path':self.path}}))
    self.connection.close()

  def add_taxa(self, values:Iterable[Tuple[int,str,int]])->None:
    """Add taxa into taxa table"""
    self.taxa.insert(self.connection, values)

  def add_taxids(self, taxids:Iterable[Tuple[int,]])->None:
    """Add taxids into taxa table"""
    self.taxa.insert_taxids(self.connection, taxids)

  def add_names(self, values:Iterable[Tuple[int,str,str]])->None:
    """Add names into taxa table"""
    self.names.insert(self.connection, values)

  def add_accessions(self, values:Iterable[Tuple[str,str,str,int]])->None:
    """Add accessions into accesssion table"""
    self.accs.insert(self.connection, values)

  def add_group(self, values:[Iterable[Tuple[int,str]]]):
    """Add group into group table"""
    self.groups.insert(self.connection, values)

  def collect_subtree(self, taxid:int, conv:Type[ncbitaxonomist.convert.taxadb.TaxaDbConverter],
                      subtree=None)->List:
    """ Collect subtree for given taxon ids. """
    self.logger.debug(json.dumps({'subtrees':{'collecting':taxid}}))
    if subtree is None:
      subtree = ncbitaxonomist.subtree.subtree.Subtree()
    if not subtree.isCollected(taxid):
      for i in self.taxa.get_subtree(self.connection, taxid):
        if not subtree.has_taxon(i['taxonid']):
          subtree.add_taxon(conv.convert_to_model({'taxid': i['taxonid'],
                                                   'parentid':i['parentid'],
                                                   'rank':i['rank']}))
        subtree.taxa[i['taxonid']].update_names({i['name']:i['type']})
    return subtree

  def get_taxa_by_name(self, names:Iterable[str],
                       conv:Type[ncbitaxonomist.convert.converter.ModelConverter],
                       query:Type[ncbitaxonomist.query.map.map.MapQuery]=None,
                       taxa:Mapping[int,ncbitaxonomist.model.datamodel.DataModel]=None)->Dict[int,ncbitaxonomist.model.datamodel.DataModel]:
    """Collect taxa by name and converter to appropriate model.

    .. todo:: Test if n.name='man' OR n.name='Bacteria OR ...' is better approach
    """
    self.logger.debug(json.dumps({'names':{'collecting':names}}))
    if taxa is None:
      taxa = {}
    taxidqry = """SELECT taxonid FROM names  WHERE name=?"""
    for i in names:
      taxid = self.connection.cursor().execute(taxidqry, (i,)).fetchone()
      if taxid is not None and taxid[0] not in taxa:
        taxa[taxid[0]] = None
    qry = """SELECT n.name, n.type, t.taxonid, t.rank, t.parentid FROM taxa t
             JOIN names n on t.taxonid=n.taxonid WHERE t.taxonid=?"""
    for i in taxa:
      for j in self.connection.cursor().execute(qry, (i,)):
        if taxa[j['taxonid']] is None:
          taxa[j['taxonid']] = conv.convert_to_model({'taxid':j['taxonid'],
                                                      'parentid':j['parentid'],
                                                      'rank':j['rank']})
        taxa[j['taxonid']].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(taxa[i])
    return taxa

  def names_to_taxid(self, names:Iterable[str])->Dict[str,int]:
    """Returns name->taxid mapping."""
    self.logger.debug(json.dumps({'names':{'mapping':names}}))
    mapping = {}
    for i in names:
      row = self.names.name_to_taxid(self.connection, i).fetchone()
      if row:
        mapping[row['name']] = int(row['taxonid'])
    return mapping

  def get_taxa_by_accessions(self, accs:Iterable[str], db:str, conv:Type[ncbitaxonomist.convert.converter.ModelConverter],
                             query:Type[ncbitaxonomist.query.map.map.MapQuery]=None)->Dict[int,ncbitaxonomist.model.datamodel.DataModel]:
    """Collect taxa by accession and converter to appropriate model."""
    self.logger.debug(json.dumps({'accessions':{'collecting':accs, 'db':db}}))
    uids = {}
    uidqry =  """SELECT db, uid FROM accessions WHERE accession=? AND db=?"""
    if not db:
      uidqry = """SELECT db, uid FROM accessions WHERE accession=? AND db LIKE ?)"""
    for i in accs:
      row = self.connection.cursor().execute(uidqry, (i, db)).fetchone()
      if row is not None:
        if row['db'] not in uids:
          uids[row['db']] = []
        uids[row['db']].append(int(row['uid']))
    stmt = """SELECT a.uid, a.accession, a.db, a.type, t.taxonid
              FROM accessions a JOIN taxa t on a.taxonid=t.taxonid
              WHERE a.uid=? and a.db=?"""
    mappings = {}
    for i in uids:
      for j in uids[i]:
        for k in self.connection.cursor().execute(stmt, (j, i)):
          if int(k['uid']) not in mappings:
            mappings[int(k['uid'])] = conv.convert_to_model({'accessions':{k['type']:k['accession']},
                                                             'taxid':k['taxonid'], 'db':k['db'],
                                                             'uid': k['uid']})
          mappings[int(k['uid'])].update_accessions({k['type']:k['accession']})
        if query and mappings:
          query.map_query(mappings[j])
    return mappings

  def get_taxa_by_taxids(self, taxids:Iterable[int], conv:Type[ncbitaxonomist.convert.converter.ModelConverter],
                         query:Type[ncbitaxonomist.query.map.map.MapQuery]=None)->Dict[int, ncbitaxonomist.model.datamodel.DataModel]:
    """Collect taxa by taxid and converter to appropriate model."""
    self.logger.debug(json.dumps({'taxids':{'collecting':taxids}}))
    qry = """SELECT t.taxonid, t.rank, t.parentid, n.name, n.type
             FROM taxa t JOIN names n on t.taxonid=n.taxonid WHERE t.taxonid=?"""
    taxa = {}
    for i in taxids:
      for j in self.connection.cursor().execute(qry, (i,)):
        if int(j['taxonid']) not in taxa:
          taxa[int(j['taxonid'])] = conv.convert_to_model({'taxid': j['taxonid'],
                                                           'parentid':j['parentid'],
                                                           'rank':j['rank']})
        taxa[int(j['taxonid'])].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(taxa[int(i)])
    return taxa

  def get_taxid_lineages(self, taxids:Iterable[int], conv:Type[ncbitaxonomist.convert.converter.ModelConverter],
                         query:Type[ncbitaxonomist.query.resolve.resolve.ResolveQuery]=None)->Dict[int, ncbitaxonomist.model.datamodel.DataModel]:
    """Collect lineage taxa for multiple taxid."""
    self.logger.debug(json.dumps({'taxids':{'collecting lineages':taxids}}))
    taxa = {}
    for i in taxids:
      if i not in taxa:
        self.get_lineage(i, conv, taxa)
      if query and taxa:
        query.resolve([i], taxa)
    return taxa

  def get_taxid_lineage(self, taxid:int, conv:Type[ncbitaxonomist.convert.converter.ModelConverter],
                        query:Type[ncbitaxonomist.query.resolve.resolve.ResolveQuery]=None,
                        taxa:Mapping[int,ncbitaxonomist.model.datamodel.DataModel]=None)->Dict[int,ncbitaxonomist.model.datamodel.DataModel]:
    """Collect lineage taxa for a single taxid."""
    self.logger.debug(json.dumps({'taxid':{'collecting lineage':taxid}}))
    if taxa is None:
      taxa = {}
    self.get_lineage(taxid, conv, taxa)
    if query and taxa:
      query.resolve([taxid], taxa)
    return taxa

  def get_lineage(self, taxid, conv:Type[ncbitaxonomist.convert.converter.ModelConverter], taxa)->None:
    """Collect lineage."""
    self.logger.debug(json.dumps({'lineage':{'taxid':taxid}}))
    for j in self.taxa.get_lineage(self.connection, taxid, self.names.name):
      if int(j['taxonid']) not in taxa:
        taxa[int(j['taxonid'])] = conv.convert_to_model({'taxid': j['taxonid'],
                                                         'parentid':j['parentid'],
                                                         'rank':j['rank']})
      taxa[int(j['taxonid'])].update_names({j['name']:j['type']})

  def remove_group(self, groupname):
    """Remove a group."""
    self.logger.debug(json.dumps({'groups':{'remove':groupname}}))
    self.groups.delete_group(self.connection, groupname)

  def remove_from_group(self, taxids, names, groupname):
    """Remove taxids and names from a given group."""
    self.logger.debug(json.dumps({'groups':{'remove':names}}))
    values = []
    seen_taxids = set()
    while taxids:
      values.append((taxids.pop(), groupname))
      seen_taxids.add(values[-1][0])
    if names:
      stmt = """SELECT taxonid FROM names WHERE name=?"""
      for i in names:
        taxid = self.connection.cursor().execute(stmt, (i,)).fetchone()[0]
        if taxid is not None and taxid not in seen_taxids:
          values.append((taxid, groupname))
          seen_taxids.add(taxid)
    seen_taxids.clear()
    self.groups.delete_from_group(self.connection, values)

  def retrieve_group_names(self)->List[sqlite3.Row]:
    """Return all group names"""
    self.logger.debug(json.dumps({'groups':{'collect':'all groupnames'}}))
    return self.groups.retrieve_names(self.connection).fetchall()

  def retrieve_group(self, groupname):
    """Return all taxids withon a given group"""
    self.logger.debug(json.dumps({'groups':{'collect':groupname}}))
    return self.groups.retrieve_group(self.connection, groupname)
