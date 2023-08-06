"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type

import ncbitaxonomist.db.dbmanager


apikey:str = None
email:str = None
db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb] = None
xmlout:bool = False
