"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


import os
import sys
import logging
import logging.config

import entrezpy.log.logger

import ncbitaxonomist.log.conf

CONFIG = {'level':'INFO'}

def configure(verbosity):
  if verbosity == 0:
    CONFIG['level'] = 'NOTSET'
  if verbosity == 1:
    CONFIG['level'] = 'INFO'
  if verbosity == 2:
    CONFIG['level'] = 'WARNING'
  if verbosity == 3:
    CONFIG['level'] = 'DEBUG'
  if verbosity > 3:
    CONFIG['level'] = 'DEBUG'
    entrezpy.log.logger.set_level('DEBUG')

def get_root():
  return 'ncbi-taxonomist'

def resolve_class_namespace(cls):
  """Resolves namespace for logger"""
  return f"{cls.__module__}.{cls.__qualname__}"

def get_class_logger(cls):
  """Prepares logger for given class """
  logger = logging.getLogger(f"{cls.__module__}.{cls.__qualname__}")
  logging.config.dictConfig(ncbitaxonomist.log.conf.default_config)
  logger.setLevel(CONFIG['level'])
  return logger

def get_logger(name=None):
  logger = None
  if name is not None:
    logger = logging.getLogger(f"{get_root()}.{name}")
  else:
    logger = logging.getLogger(get_root())
  if logger is None:
    sys.exit("Logger setup failed.")
  logging.config.dictConfig(ncbitaxonomist.log.conf.default_config)
  logger.setLevel(CONFIG['level'])
  return logger
