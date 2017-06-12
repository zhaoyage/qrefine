from __future__ import division
import os
import iotbx.pdb
from scitbx.array_family import flex
from libtbx import easy_pickle
import time
import run_tests
import libtbx.load_env
from libtbx.test_utils import approx_equal

qrefine = libtbx.env.find_in_repositories("qrefine")
qr_unit_tests_data = os.path.join(qrefine,"tests","unit","data_files")

def run(prefix = "tst_15"):
  """
  Exercise gradients match:
    - small vs large box:
      -- using clustering vs not using clustering.
  """
  #for restraints in ["cctbx","qm"]:
  for restraints in ["cctbx",]:
  # XXX qm option is not supposed to work fulfull the test with 2ona_box_S
  # XXX qm option is currently suspected to be broken for 2ona_box_L
    for data_file_prefix in ["2ona_box_L", "2ona_box_S"]:
      common_args = ["restraints=%s"%restraints, "mode=opt", "nproc=1",
                     "qm_engine_name=mopac"]
      args = common_args+["clustering=false","dump_gradients=cluster_false.pkl"]
      r = run_tests.run_cmd(prefix,
        args     = args,
        pdb_name = os.path.join(qr_unit_tests_data,"%s.pdb"%data_file_prefix),
        mtz_name = os.path.join(qr_unit_tests_data,"%s.mtz"%data_file_prefix))

      args = common_args+["clustering=true", "dump_gradients=cluster_true.pkl"]
      r = run_tests.run_cmd(prefix,
        args     = args,
        pdb_name = os.path.join(qr_unit_tests_data,"%s.pdb"%data_file_prefix),
        mtz_name = os.path.join(qr_unit_tests_data,"%s.mtz"%data_file_prefix))

      #
      g1 = flex.vec3_double(easy_pickle.load("cluster_false.pkl"))
      g2 = flex.vec3_double(easy_pickle.load("cluster_true.pkl"))
      assert g1.size() == g2.size()
      diff = g1-g2
      if(0):
        for i, diff_i in enumerate(diff):
          print i+1, diff_i, g1[i], g2[i]
        print
      assert approx_equal(diff.max(), [0,0,0])

if __name__ == '__main__':
  t0 = time.time()
  prefix = "tst_15"
  run(prefix)
  print prefix + ":  OK  " + "Time: %6.2f (s)" % (time.time() - t0)