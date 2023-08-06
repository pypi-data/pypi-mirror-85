"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Type, Mapping


import ncbitaxonomist.model.accession
import ncbitaxonomist.convert.converter

class DbAccessionConverter(ncbitaxonomist.convert.converter.ModelConverter):
  """Class implementing a converter for accession attributes and models"""

  def convert_to_model(self, attributes:Mapping[str,any], srcdb=None)->Type[ncbitaxonomist.model.accession.Accession]:
    """Converts local database attributes to accession model"""
    del srcdb #Unused
    return ncbitaxonomist.model.accession.Accession(attributes)

  def convert_from_model(self, model:Type[ncbitaxonomist.model.accession.Accession], outdict=None)->Dict[str,str]:
    """Converts accession model to attributes"""
    del outdict #Unused
    return model.get_attribues()
