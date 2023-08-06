"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import ncbitaxonomist.config

import entrezpy.conduit


class EntrezTaxonomyQuery:

  conduit = entrezpy.conduit.Conduit(ncbitaxonomist.config.email,
                                     ncbitaxonomist.config.apikey)

  @staticmethod
  def query_taxids(taxids, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    pipe.add_fetch({'db':'taxonomy', 'id':taxids, 'mode':'xml'}, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()

  @staticmethod
  def query_names(names, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    sid = pipe.add_search({'db':'taxonomy', 'term':' OR '.join("\"{}\"".format(x) for x in names)})
    pipe.add_fetch({'mode':'xml'}, dependency=sid, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()

  @staticmethod
  def query_accessions(accessions, database, analyzer):
    pipe = EntrezTaxonomyQuery.conduit.new_pipeline()
    if database in set(['nuccore', 'nucest', 'nucgss', 'popset', 'protein']):
      pipe.add_summary({'mode':'json', 'db':database, 'id':accessions}, analyzer=analyzer)
    else:
      sid = pipe.add_search({'db':database, 'term':' OR '.join(str(x) for x in accessions)})
      pipe.add_summary({'mode':'json'}, dependency=sid, analyzer=analyzer)
    EntrezTaxonomyQuery.conduit.run(pipe).get_result()
