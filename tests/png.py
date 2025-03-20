"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing for png only
"""

import filecmp
from responsiveimage import __main__

def test_png():
  """
  Test
  """
  srcdir = 'tests/data/png'
  refdir = srcdir + '/' + 'ref'
  # tempdir = tempfile.gettempdir()
  tempdir = 'tests/results/png'
  __main__.main([ '--src-dir', srcdir, '--dst-dir', tempdir, '--force' ])

  # compare binary files
  for file in [ 'lpo' ]:
    assert filecmp.cmp(refdir+'/'+file+'.png', tempdir+'/'+file+'.png', shallow=True), f"{file}"
