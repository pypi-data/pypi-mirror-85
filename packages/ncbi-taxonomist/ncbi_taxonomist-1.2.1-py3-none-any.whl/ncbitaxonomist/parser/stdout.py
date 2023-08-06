"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import sys

import ncbitaxonomist.convert.ncbitaxon
import ncbitaxonomist.model.taxon
import ncbitaxonomist.model.accession
import ncbitaxonomist.log.logger


class StdoutParser:
  """
  Parse taxonomist json results from STDOUT. Onr result per line is expected.
  The parser is intended to parse only one line. The loop over  stdin input
  needs to be imlemented by the method parsing the data.
  """
  def __init__(self):
    self.logger = ncbitaxonomist.log.logger.get_class_logger(StdoutParser)
    self.taxonconverter = ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()

  def parse(self, stdin_line):
    line = json.loads(stdin_line.strip())
    mode = line.get('mode')
    if mode is None:
      return self.parse_taxon(line)
    if mode == 'mapping':
      return self.parse_mapping(line)
    if mode == 'resolve':
      return self.parse_lineage(line)
    sys.exit(self.logger.error(json.dumps({'unknown input format':line})))

  def parse_taxon(self, line):
    self.logger.debug(json.dumps({'parsing':'taxon', 'attributes':line}))
    if 'taxid' not in line or 'rank' not in line or 'parentid' not in line or 'names' not in line:
      self.logger.error(json.dumps({'parsing':'taxon', 'bad format':line}))
    return line

  def parse_mapping(self, line):
    self.logger.debug(json.dumps({'parsing':'mapping', 'attributes':line}))
    cast = line.get('cast')
    if cast is None:
      sys.exit(self.logger.error(json.dumps({'badly formatted mapping result':line})))
    if cast == 'accs':
      return {'query':line.get('query'), 'accession':line.get('accession')}
    elif cast == 'taxon':
      return self.parse_taxon(line.get('taxon'))
    else:
      sys.exit(self.logger.error(json.dumps({'Unknown mapping cast':cast, 'input':line})))

  def parse_lineage(line):
    self.logger.debug(json.dumps({'parsing':'lineage', 'attributes':line}))
    pass
