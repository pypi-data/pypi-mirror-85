"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import sys
import xml.etree.ElementTree


import ncbitaxonomist.log.logger
import ncbitaxonomist.formatter.base

class XmlFormatter(ncbitaxonomist.formatter.base.BaseFormatter):

  def __init__(self):
    super().__init__(logcls=XmlFormatter)

  def taxon_element(self, model):
    if model.cast != 'taxon':
      sys.exit(self.logger.error(json.dumps({'wrong model cast for taxon':model.cast})))
    elem = xml.etree.ElementTree.Element('taxon')
    xml.etree.ElementTree.SubElement(elem, 'taxid').text = str(model.taxid())
    xml.etree.ElementTree.SubElement(elem, 'rank').text = model.rank()
    xml.etree.ElementTree.SubElement(elem, 'name').text = model.get_name_by_type()
    xml.etree.ElementTree.SubElement(elem, 'parentid').text = str(model.parent())
    n = xml.etree.ElementTree.SubElement(elem, 'names')
    for i in model.names:
      name = xml.etree.ElementTree.Element('name')
      name.text = i
      name.set('type', model.names[i])
      n.append(name)
    return elem

  def accession_element(self, model):
    if model.cast != 'accs':
      sys.exit(self.logger.error(json.dumps({'wrong model cast for accession':model.cast})))
    elem = xml.etree.ElementTree.Element('accession')
    xml.etree.ElementTree.SubElement(elem, 'taxid').text = str(model.taxid())
    xml.etree.ElementTree.SubElement(elem, 'uid').text = str(model.uid)
    xml.etree.ElementTree.SubElement(elem, 'database').text = model.db
    accs = xml.etree.ElementTree.SubElement(elem, 'accessions')
    for i in model.accessions:
      xml.etree.ElementTree.SubElement(accs, i).text = str(model.accessions[i])
    return elem

  def mapping_query(self, query, cast):
    qry = xml.etree.ElementTree.Element('query')
    qry.text = query
    qry.set('cast', cast)
    elem = xml.etree.ElementTree.Element('mapping')
    elem.append(qry)
    return elem

  def lineage_element(self, lineage):
    elem = xml.etree.ElementTree.Element('lineage')
    for i in lineage:
      elem.append(self.taxon_element(i))
    return elem

  def query_element(self, attrib_key, attrib_value, query_element=None):
    query = xml.etree.ElementTree.Element('query')
    query.set('value', attrib_value)
    query.set('cast', attrib_key)
    if query_element is not None:
      query.append(query_element)
    return query

  def format_collection(self, model):
    self.write_tree(xml.etree.ElementTree.ElementTree(self.taxon_element(model)))

  def format_mapping(self, query, model, qrycast):
    qry = None
    if model.cast == 'taxon':
      qry = self.mapping_query(query, model.cast)
      qry.append(self.taxon_element(model))
    else:
      qry = self.mapping_query(query, 'accession')
      qry.append(self.accession_element(model))
    self.write_tree(xml.etree.ElementTree.ElementTree(qry))

  def format_resolve(self, querycast, query, model, lineage):
    elem = xml.etree.ElementTree.Element('resolve')
    if model.cast == 'accs':
      elem.append(self.query_element('accession', query, self.accession_element(model)))
    else:
      elem.append(self.query_element(querycast, query, self.taxon_element(model)))
    elem.append(self.lineage_element(lineage))
    self.write_tree(xml.etree.ElementTree.ElementTree(elem))

  def format_subtrees(self, lineages, taxid, name):
    elem = xml.etree.ElementTree.Element('subtree')
    if name is not None:
      elem.append(self.query_element('name', name))
    else:
      elem.append(self.query_element('taxid', str(taxid)))
    for i in lineages:
      stree = xml.etree.ElementTree.Element('tree')
      for j in i:
        stree.append(self.taxon_element(j))
      elem.append(stree)
    self.write_tree(xml.etree.ElementTree.ElementTree(elem))

  def write_tree(self, tree):
    tree.write(sys.stdout, encoding='unicode')
    print()
