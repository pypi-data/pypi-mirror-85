"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sqlite3
from typing import Iterable, Tuple, Type

import ncbitaxonomist.db.table.basetable

class GroupTable(ncbitaxonomist.db.table.basetable.BaseTable):

  def __init__(self, database:str):
    super().__init__(name='groups', database=database)

  def create(self, connection:Type[sqlite3.Connection])->__qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS groups
              (id        INTEGER PRIMARY KEY,
                taxonid INT NOT NULL,
                grp      TEXT NOT NULL,
                FOREIGN KEY (taxonid) REFERENCES taxa(taxonid) ON DELETE CASCADE,
                UNIQUE(taxonid, grp))"""
    connection.cursor().execute(stmt)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON groups (taxonid, grp)""".format(self.idx)
    connection.cursor().execute(stmt)

  def insert(self, connection:Type[sqlite3.Connection], values:Iterable[Tuple[int,str]])->None:
    stmt = """INSERT OR IGNORE INTO groups (taxonid, grp) VALUES (?,?)"""
    connection.cursor().executemany(stmt, values)
    connection.commit()

  def delete_group(self, connection:Type[sqlite3.Connection], groupname:str)->None:
    stmt = """DELETE FROM groups WHERE  grp=?"""
    connection.cursor().execute(stmt, (groupname,))
    connection.commit()

  def delete_from_group(self, connection:Type[sqlite3.Connection], values:Iterable[Tuple[str,int]])->None:
    stmt = """DELETE FROM groups WHERE taxonid=? and grp=?"""
    connection.cursor().executemany(stmt, values)
    connection.commit()

  def retrieve_names(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT DISTINCT(grp) AS name FROM groups")

  def retrieve_group(self, connection:Type[sqlite3.Connection], groupname:str):
    if groupname is None:
      stmt = """SELECT grp AS name, taxonid FROM groups ORDER BY name"""
      return connection.cursor().execute(stmt)
    stmt = """SELECT grp AS name, taxonid FROM groups WHERE grp=? ORDER BY name"""
    return connection.cursor().execute(stmt, (groupname,))
