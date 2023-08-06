"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type


import ncbitaxonomist.model.accession


class AccessionCache:
  """
  Class to handle caching of accessions. Accessions are stored mapping
  accessions as key and class:`ncbitaxonomist.model.accession.AccessionData` as
  value.
  """

  def __init__(self):
    self.accessions = {}

  def cache(self, acc:Type[ncbitaxonomist.model.accession.Accession]):
    """Caches accession"""
    accs = acc.get_accessions()
    for i in accs:
      if accs[i] not in self.accessions:
        self.accessions[accs[i]] = acc

  def incache(self, name=None, taxid=None):
    """Tests if given accession is in cache."""
    del taxid # Unused
    return name in self.accessions

  def is_empty(self):
    """Tests if cache is empty."""
    if self.accessions:
      return False
    return True

  def get_accession(self, acc)->Type[ncbitaxonomist.model.accession.Accession]:
    """Returns given or all taxids in cache"""
    if acc in self.accessions:
      return self.accessions[acc]
    return None
