"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import os
import sys
from typing import Type

import entrezpy.log.logger

import ncbitaxonomist.config
import ncbitaxonomist.cache.cache
import ncbitaxonomist.db.dbimporter
import ncbitaxonomist.db.dbmanager
import ncbitaxonomist.log.logger


entrezpy.log.logger.set_level('WARNING')
logger = ncbitaxonomist.log.logger.get_logger(__name__)

def configure(args):
  ncbitaxonomist.config.apikey:str = args.apikey
  ncbitaxonomist.config.email = args.email
  ncbitaxonomist.config.xmlout = args.xml
  ncbitaxonomist.log.logger.configure(args.verbose)
  logger.debug(json.dumps({'config':{'apikey':ncbitaxonomist.config.apikey,
                                     'email':ncbitaxonomist.config.email,
                                     'xmlout': ncbitaxonomist.config.xmlout,
                                     'verbosity': args.verbose}}))

class NcbiTaxonomist:
  """
  Setup taxonomist run. Instantiate the cache, connect to a local database
  and store verbosity.
  """

  cache = ncbitaxonomist.cache.cache.Cache()

  def __init__(self, dbpath:str=None):
    """Ctor to setup local database and create logger."""
    self.db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb] = None
    if dbpath:
      self.db = ncbitaxonomist.db.dbmanager.TaxonomyDb(dbpath)


  def import_to_db(self):
    """Import data to local taxonomy database."""
    ncbitaxonomist.db.dbimporter.import_stdin(self.db)
