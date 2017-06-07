from __future__ import division
from test_reg_00_base import test_base

class test_finalise(test_base):

  def check_assertions(self,result):
    """
    Exercise structure completion by finalise.py
    """
    result_db = self.db.old.find_one({"pdb_code": result.pdb_code})
    assert result_db['charge']     == result.charge
    assert result_db['super_cell'] == result.super_cell
    assert result_db['completion'] == result.completion
    assert result_db['finalise']   == result.capping
    assert result_db['failing']    == result.failing
  
  def insert(self,result):
    self.db.old.insert_one({"pdb_code"        : result.pdb_code,
                            "chunk"           : result.clusters,
                            "chunks"          : result.chunks,
                            "chunk_sizes"     : result.chunk_sizes,
                            "num_of_chunks"   : result.num_of_chunks,
                            "num_of_clusters" : result.num_of_clusters})

