"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
from typing import Mapping

import ncbitaxonomist.config
import ncbitaxonomist.formatter.jsonformatter
import ncbitaxonomist.formatter.xmlformatter


def json_stdout(data:Mapping[str,str]):
  """Prints input dict as JSON to stdout"""
  sys.stdout.write(json.dumps(data, separators=(',', ':'))+'\n')

def no_rank():
  """Returns the value for taxa without ranks, works as a constant since Python
     has no constants"""
  return 'NA'

def get_formatter():
  """Returns approprate output formatter."""
  if ncbitaxonomist.config.xmlout:
    return ncbitaxonomist.formatter.xmlformatter.XmlFormatter()
  return ncbitaxonomist.formatter.jsonformatter.JsonFormatter()
