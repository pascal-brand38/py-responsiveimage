"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing for png only
"""

import filecmp
import getresdir
from responsiveimage import __main__

def test_png():
  """
  Test
  """
  srcdir = 'tests/data/png'
  refdir = srcdir + '/' + 'ref'
  resdir = getresdir.resDir('png')
  __main__.main([ '--src-dir', srcdir, '--dst-dir', resdir, '--force' ])

  # compare binary files
  for file in [ 'lpo' ]:
    assert filecmp.cmp(refdir+'/'+file+'.png', resdir+'/'+file+'.png', shallow=True), f"{file}"
