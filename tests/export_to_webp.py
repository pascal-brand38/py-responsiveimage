"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing for png only
"""

import filecmp
import getresdir
from responsiveimage import __main__

def test_export_to_webp():
  """
  Test
  """
  srcdir = 'tests/data/export_to_webp'
  refdir = srcdir + '/' + 'ref'
  resdir = getresdir.resDir('export_to_webp')

  __main__.main([ '--src-dir', srcdir, '--dst-dir', resdir, '--export-to-webp', '--size', '256,128', '--force' ])

  # compare binary files
  for file in [
    'greenpeace-128.webp', 'greenpeace-256.webp',
    'lpo-128.webp', 'lpo-256.webp',
    'wwf-128.jpg', 'wwf-128.webp', 'wwf-256.jpg', 'wwf-256.webp',
  ]:
    assert filecmp.cmp(refdir+'/'+file, resdir+'/'+file, shallow=True), f"{file}"
  for file in [
    'lpo-128', 'lpo-256',
  ]:
    assert filecmp.cmp(refdir+'/'+file+'.png', resdir+'/'+file+'.png', shallow=True) or filecmp.cmp(refdir+'/'+file+'-2.png', resdir+'/'+file+'.png', shallow=True), f"{file}"
