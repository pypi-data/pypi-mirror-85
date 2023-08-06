"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Mapping
import json


def int_attribute(attribute):
  """Enforce int for attribute"""
  if attribute is None:
    return attribute
  return int(attribute)

def standardize_attributes(attributes:Mapping[str,any]):
  """
  Convert None into empty dictionary. See Important warning at
  https://docs.python.org/3/tutorial/controlflow.html#default-argument-values
  """
  if attributes is None:
    attributes = {}
  return attributes

class DataModel:
  """Base class for data models."""

  @classmethod
  def new(cls, attributes:Mapping[str,any]=None)->__qualname__:
    """Return new instance with given attributes"""
    return cls(attributes)

  @classmethod
  def new_from_json(cls, json_attributes:str)->__qualname__:
    """Return new instance with attributes encoded in JSON """
    return cls.new(json.loads(json_attributes))

  def __init__(self, cast, attributes:Mapping=None):
    """Ctor. Set attributes as required."""
    self.cast = cast
    self.taxonid = None

  def taxid(self):
    return self.taxonid

  def get_attributes(self)->Dict[str,any]:
    """Return taxon attributes as dictionary."""
    raise NotImplementedError


