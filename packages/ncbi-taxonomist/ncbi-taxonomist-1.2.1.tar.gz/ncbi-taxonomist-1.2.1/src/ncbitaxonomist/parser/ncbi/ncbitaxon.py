"""
..
  Copyright 2018, 2019 The University of Sydney

.. module:: ncbi_taxonomist/ncbiparser/ncbitaxon.py
   :synopsis: Exports class NcbiTaxon implementing a basic taxonomical unit for
   NCBI taxa.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import json

class NcbiTaxon:

  """ Implementing a basic taxon with NCBI attributes

  :param dict attributes: NCBI taxon attributes as found in their TaxoXML
  """

  class OtherName:

    class Name:

      def __init__(self):
        self.cde = None
        self.name = None
        self.unique_name = None

    def __init__(self):
      self.genbank_common = None
      self.genbank_acronym = None
      self.blast = None
      self.equivalents = []
      self.synonyms = []
      self.acronyms = []
      self.anamorphs = []
      self.includes = []
      self.commons = []
      self.misnomers = []
      self.teleomorphs = []
      self.genbank_synonyms = []
      self.genbank_anamorphs = []
      self.cde_names = []
      self.names = {}

    def add_name(self, name, name_type):
      self.names[name] = name_type

    def new_cde_name(self):
      self.cde_names.append(NcbiTaxon.OtherName.Name())
      return self.cde_names[-1]

    def dump(self):
      return {'names' : self.names,
              'cde_names' : [{'cde':x.cde, 'name':x.name, 'uniqname':x.unique_name} for x in self.cde_names]}
  class Date:

    def __init__(self):
      self.pub = None
      self.create = None
      self.update = None

  class GeneticCode:

    def __init__(self):
      self.id = None
      self.name = None

  def __init__(self, isQuery=False):
    self.taxid = None
    self.rank = None
    self.scientific_name = None
    self.parent_taxid = None
    self.division = None
    self.isQuery = isQuery
    self.genetic_code = NcbiTaxon.GeneticCode()
    self.mitogenetic_code = NcbiTaxon.GeneticCode()
    self.aliases = []
    self.other_names = NcbiTaxon.OtherName()
    self.dates = NcbiTaxon.Date()

  def hasAlias(self):
    if self.aliases:
      return True
    return False

  def get_aliases(self):
    return self.aliases

  def add_parent(self, parent_taxid):
    self.parent_taxid = int(parent_taxid)

  def get_parent_taxid(self):
    if self.parent_taxid:
      return int(self.parent.taxid)
    return None

  def attribute_dict(self):
    attribs = {'taxid': self.taxid,
               'rank' : self.rank,
               'scientific_name' : self.scientific_name,
               'other_names': self.other_names.dump(),
               'division' : self.division,
               'parent_taxid' : self.parent_taxid,
               'aliases' : self.aliases,
               'genetic_code' : None,
               'mitogenetic_code_id' : None,
               'dates' : {'pdate':self.dates.pub,
                          'mtime':self.dates.update,
                          'ctime':self.dates.create},
               'aliases' : None}
    if self.genetic_code.id:
      attribs.update({'genetic_code' : {self.genetic_code.name: self.genetic_code.id}})
    if self.mitogenetic_code.id:
      attribs.update({'mitogenetic_code_id' : {self.mitogenetic_code.name:self.mitogenetic_code.id}}),
    if self.aliases:
      attribs.update({'aliases' : self.aliases})
    return attribs

  def as_json(self):
    return json.dumps(self.attribute_dict())

  def dump(self):
    return self.attribute_dict()
