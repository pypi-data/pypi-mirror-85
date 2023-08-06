"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sqlite3
from typing import Tuple, Type

class BaseTable:
  """Implements a basic table in a taxonomist database."""

  def __init__(self, name:str, database:str):
    """
      Ctor for a taxonomist table

      :param name: table name
      :param database: database path
    """
    self.name = name
    self.database = database
    self.idx = "{}_idx".format(self.name)

  def create(self, connection:Type[sqlite3.Connection])->__qualname__:
    """Virtual function to create table"""
    raise NotImplementedError("Implement create() method")

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    """Virtual function to create table index"""
    raise NotImplementedError("Implement create_index() method")

  def insert(self, connection:Type[sqlite3.Connection], values:Tuple)->None:
    """Virtual function to insert rows"""
    raise NotImplementedError("Implement insert() method")
