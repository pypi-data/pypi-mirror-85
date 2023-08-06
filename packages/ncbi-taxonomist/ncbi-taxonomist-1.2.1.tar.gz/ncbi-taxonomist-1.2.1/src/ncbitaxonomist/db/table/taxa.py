"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sqlite3
from typing import Iterable, Tuple, Type

import ncbitaxonomist.db.table.basetable

class TaxaTable(ncbitaxonomist.db.table.basetable.BaseTable):
  """Implements taxa table for local taxonomy database."""

  def __init__(self, database:str):
    super().__init__(name='taxa', database=database)

  def create(self, connection:Type[sqlite3.Connection])->__qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS taxa
              (id           INTEGER PRIMARY KEY,
               taxonid     INT NOT NULL,
               rank         TEXT NULL,
               parentid    INT NULL,
               UNIQUE(taxonid))"""
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON taxa (taxonid)""".format(self.idx)
    connection.cursor().execute(stmt)

  def insert(self, connection:Type[sqlite3.Connection], taxavalues:Iterable[Tuple[int,str,int]])->None:
    stmt = """INSERT INTO taxa (taxonid, rank, parentid) VALUES (?,?,?)
              ON CONFLICT (taxonid) WHERE parentid is NULL
              DO UPDATE SET parentid=excluded.parentid,rank=excluded.rank"""
    connection.cursor().executemany(stmt, taxavalues)
    connection.commit()

  def insert_taxids(self, connection:Type[sqlite3.Connection], taxids:Iterable[int])->None:
    stmt = """INSERT OR IGNORE INTO taxa (taxonid) VALUES (?)"""
    connection.cursor().executemany(stmt, taxids)
    connection.commit()

  def get_taxids(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("""SELECT taxonid FROM taxa""")

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT taxonid, rank, name, parentid FROM taxa")

  def get_lineage(self, connection:Type[sqlite3.Connection], taxid:int, name_table:str)->Type[sqlite3.Cursor]:
    """Recursive construction of lineage from given taxid to highest parent."""
    stmt = """WITH RECURSIVE parent(taxonid) AS
      (SELECT taxonid FROM taxa WHERE taxonid=?  -- initial lookup
       UNION ALL                                   -- start recursion
       SELECT t.parentid FROM taxa t, parent      -- subquery
       WHERE  t.taxonid=parent.taxonid)
      SELECT t.taxonid, t.rank, t.parentid, n.name, n.type FROM taxa t -- select recursion result
      JOIN parent p ON t.taxonid=p.taxonid
      JOIN {0} n ON t.taxonid=n.taxonid""".format(name_table)
    return connection.cursor().execute(stmt, (taxid,))

  def get_subtree(self, connection:Type[sqlite3.Connection], taxid:int)->Type[sqlite3.Cursor]:
    """Depth first search of taxon ids to find the subtree of taxid"""
    stmt = """WITH RECURSIVE subtree(taxonid, depth, rank) AS
      (SELECT ti.taxonid, 0, ti.rank FROM taxa ti WHERE ti.taxonid=? -- initial lookup
       UNION ALL                                                      -- start recursion
       SELECT tq.taxonid, st.depth+1, tq.rank FROM taxa tq            -- subquery
       JOIN subtree st ON tq.parentid=st.taxonid
       ORDER BY 2 DESC)                                               -- do dfs
       SELECT rst.taxonid, rst.rank, t.parentid, n.name, n.type FROM subtree rst -- select recursed results
       JOIN names n on rst.taxonid=n.taxonid
       JOIN taxa t on t.taxonid=rst.taxonid"""
    return connection.cursor().execute(stmt, (taxid,))
