"""
..
  Copyright 2018, 2019 The University of Sydney

.. module:: ncbi_taxonomist.ncbiparser
   :synopsis:  Exports class NcbiTaxoXmlParser implementing parsing NCBI XML
              taxonomy files

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import xml.etree.ElementTree as ET


import ncbitaxonomist.parser.ncbi.ncbitaxon


class TaxoXmlParser:
  """ Parse XML taxonomy file and assemble lineages. The first encountered taxon
  in a NCBI taxonomy XML file is considered a query and stored separately.

  :param dict taxa: reference to storage of already encountered taxids
  :param dict alias: reference to store aliases
  """

  taxa = {}
  alias = {}

  class Result:

    def __init__(self):
      self.queries = set()
      self.taxa = {}

    def add_taxon(self, taxon):
      if taxon.taxid not in self.taxa:
        self.taxa[taxon.taxid] = taxon
        if taxon.isQuery:
          self.queries.add(taxon.taxid)

  def __init__(self, taxa=None, alias=None):
    self.taxa = TaxoXmlParser.taxa if taxa is None else taxa
    self.alias = TaxoXmlParser.alias if alias is None else alias

  def parse(self, xml):
    """
    :param xml: NCBI taxonomy XML
    :type xml: file-like object
    :return: query result
    :rtype: class:`NcbiTaxoXmlParser.Result`
    https://effbot.org/zone/element-iterparse.htm
    """
    result = TaxoXmlParser.Result()
    context = iter(ET.iterparse(xml, events=("start", "end")))
    status = 0
    taxon = None
    parent = None
    isQuery = True
    event, root = next(context)
    event, elem = next(context)
    qry = None
    while True:
      if status == 0:
        if elem.tag == 'Taxon' and event == 'start':
          taxon = ncbitaxonomist.parser.ncbi.ncbitaxon.NcbiTaxon(isQuery=isQuery)
          event, elem = next(context)
        elif elem.tag == 'Taxon' and event == 'end':
          parent = self.process_taxon(taxon, parent, result)
          event, elem = next(context)
        elif elem.tag == 'OtherNames' and event == 'start':
          status = 2
        elif elem.tag == 'LineageEx' and event == 'start':
          isQuery = False
          qry = taxon
          event, elem = next(context)
        elif elem.tag == 'LineageEx' and event == 'end':
          isQuery = True
          taxon = qry
          event, elem = next(context)
        elif elem.tag == 'AkaTaxIds' and event == 'start':
          status = 3
        elif elem.tag == 'TaxaSet' and event == 'end':
          return result
        else:
          self.parse_taxon(taxon, event, elem)
          event, elem = next(context)

      elif status == 2:
        if elem.tag == 'OtherNames' and event == 'end':
          status = 0
        if elem.tag == 'Name' and event == 'start':
          taxon.other_names.new_cde_name()
          status = 4
        else:
          self.parse_other_name(taxon, event, elem)
          event, elem = next(context)

      elif status == 3:
        if elem.tag == 'TaxId' and event == 'end':
          taxon.aliases.append(int(elem.text))
          event, elem = next(context)
        elif elem.tag == 'AkaTaxIds' and event == 'end':
          status = 0
        else:
          event, elem = next(context)

      elif status == 4:
        if elem.tag == 'Name' and event == 'end':
          status = 2
        if elem.tag == 'ClassCDE':
          taxon.other_names.cde_names[-1].cde = elem.text
        if elem.tag == 'DispName':
          taxon.other_names.cde_names[-1].name = elem.text
        if elem.tag == 'UniqueName':
          taxon.other_names.cde_names[-1].unique_name = elem.text
        event, elem = next(context)
      else:
        event, elem = next(context)

  def process_taxon(self, taxon, parent, result):
    """Check if taxon has a parent node and update where neccesary.
    Returns the taxon as the new parent since the next taxid will be the
    child of this taxon in the XML."""
    result.add_taxon(taxon)
    if parent:
      taxon.add_parent(parent.taxid)
    if taxon.taxid not in self.taxa:
      self.taxa[taxon.taxid] = taxon
    if taxon.hasAlias():
      for i in taxon.aliases:
        self.alias[i] = taxon.taxid
        self.taxa[i] = taxon
    if taxon.isQuery:
      return None
    return self.taxa[taxon.taxid]

  def parse_other_name(self, taxon, event, elem):
    if event == 'end' and elem.tag != 'OtherNames':
      taxon.other_names.add_name(elem.text, elem.tag)

  def parse_taxon(self, taxon, event, elem):
    """
    Parse a taxon node in NCBI Taxonomy XML entries and reconstruct lineage.

    :param event: 'start' or 'stop'
    :type event: :class:`xml.etree.ElementTree` event,
    :param elem: XML tag
    :type elem:  :class:`xml.etree.ElementTree` element
    :param dict attribs: store taxon attributes
    """
    if event == 'end':
      if elem.tag == 'TaxId':
        taxon.taxid = int(elem.text)
      if elem.tag == 'ScientificName':
        taxon.scientific_name = elem.text
      if elem.tag == 'ParentTaxId':
        taxon.parent_taxid = int(elem.text)
      if elem.tag == 'Rank':
        taxon.rank = elem.text
      if elem.tag == 'Division':
        taxon.division = elem.text
      if elem.tag == 'GCId':
        taxon.genetic_code.id = int(elem.text)
      if elem.tag == 'GCName':
        taxon.genetic_code.name = elem.text
      if elem.tag == 'MGCId':
        taxon.mitogenetic_code.id = int(elem.text)
      if elem.tag == 'MGCName':
        taxon.mitogenetic_code.name = elem.text
      if elem.tag == 'CreateDate':
        taxon.dates.create = elem.text
      if elem.tag == 'UpdateDate':
        taxon.dates.update = elem.text
      if elem.tag == 'PubDate':
        taxon.dates.pub = elem.text
