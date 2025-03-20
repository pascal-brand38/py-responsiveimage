"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing for cropping
"""

import filecmp
import tempfile
from responsiveimage import __main__

def test_export_to_webp():
  """
  Test cropping
  """
  srcdir = 'tests/data/crop'
  refdir = srcdir + '/' + 'ref'
  # tempdir = tempfile.gettempdir()
  tempdir = 'tests/results/crop'
  __main__.main([
    '--src-dir', srcdir,
    '--dst-dir', tempdir,
    '--crop', '150,50,300,170',
    '--height', '100',
    '--add-name', '_crop',
    '--force' ])

  # compare binary files
  for file in [
    'wwf_crop.jpg'
  ]:
    assert filecmp.cmp(refdir+'/'+file, tempdir+'/'+file, shallow=True), f"{file}"
