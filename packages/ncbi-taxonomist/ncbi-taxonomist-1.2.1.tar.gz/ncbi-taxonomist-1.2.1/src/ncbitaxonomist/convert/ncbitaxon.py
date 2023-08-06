"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping, Type


import ncbitaxonomist.convert.converter
import ncbitaxonomist.convert.convertermap
import ncbitaxonomist.model.taxon


class NcbiTaxonConverter(ncbitaxonomist.convert.converter.ModelConverter):
  """
  Converts NCBI taxon attributes in class:`ncbitaxonomist.model.taxon.Taxon`
  instances and vice versa
  """

  exclude = set(['misspelling', 'authority'])

  def convert_to_model(self, attributes:Mapping, srcdb=None)->Type[ncbitaxonomist.model.taxon.Taxon]:
    """
    Convert NCBI taxon attributes into class:`ncbitaxonomist.model.taxon.Taxon`.
    """
    del srcdb # Unused
    mattribs = {'names':{attributes.pop('scientific_name'):'scientific_name'}}
    self.map_inattributes(mattribs, attributes, ncbitaxonomist.convert.convertermap.attributes)
    mattribs['names'].update(attributes['other_names'].pop('names', None))
    model = ncbitaxonomist.model.taxon.Taxon(mattribs)
    if 'cde_names' in attributes['other_names']:
      self.add_cdenames(model, attributes['other_names'].pop('cde_names'))
    return model

  def convert_from_model(self, model:Type[ncbitaxonomist.model.taxon.Taxon], outdict=None)->Dict:
    """Convert class:`ncbitaxonomist.model.taxon.Taxon` into dict attributes"""
    del outdict # Unused
    return model.get_attributes()

  def add_cdenames(self, model, cdenames):
    """Format CDE tags from NCBI format"""
    for i in cdenames:
      if i['cde'] not in NcbiTaxonConverter.exclude:
        model.names[i['name']] = i['cde']
        if i['uniqname']:
          model.names[i['uniqname']] = 'uniqname'
