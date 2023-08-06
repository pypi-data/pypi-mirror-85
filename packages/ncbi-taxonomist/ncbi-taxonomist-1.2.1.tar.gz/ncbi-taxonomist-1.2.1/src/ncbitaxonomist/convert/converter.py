"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping, Type

import ncbitaxonomist.model.datamodel

class ModelConverter:
  """Base class for converters between attributes and models."""

  def __init__(self):
    pass

  def convert_to_model(self, attributes:Mapping[str,any], srcdb=None)->Type[ncbitaxonomist.model.datamodel.DataModel]:
    """Virtual method converts attributes to model"""
    raise NotImplementedError

  def convert_from_model(self, model:Type[ncbitaxonomist.model.datamodel.DataModel], outdict:Mapping=None)->Dict:
    """Virtual method converts model to attributes"""
    raise NotImplementedError

  def map_inattributes(self, mattribs:Mapping[str,any], indata:Mapping[str,any],
                       convmap:Mapping[str,str], switch:bool=False):
    """Map input attributes to wanted model attributes"""
    for i in convmap:
      if i in indata and convmap[i] is None and indata[i]:
        if switch:
          mattribs[indata.pop(i)] = i
        else:
          mattribs[i] = indata.pop(i)
      if i in indata and convmap[i] is not None and indata[i]:
        if switch:
          mattribs[indata.pop(i)] = convmap[i]
        else:
          mattribs[convmap[i]] = indata.pop(i)
