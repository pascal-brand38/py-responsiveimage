"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing for mp4 only
"""

import os
import tempfile
import filetype
from responsiveimage import __main__

def check_file(refdir, resdir, file, ext):
  """
  TODO
  """
  res = resdir + '/' + file
  ref = refdir + '/' + file
  sizeRes = os.path.getsize(res)
  sizeRef = os.path.getsize(ref)
  assert filetype.guess(res).extension == ext, f"extension of {file}"
  diff = abs(sizeRes - sizeRef) / sizeRes
  assert diff<0.25 , f"size res {sizeRes} vs size ref {sizeRef}  diff size {100*diff}%"

def test_mp4():
  """
  Test of a mp4
  """
  srcdir = 'tests/data/mp4'
  refdir = srcdir + '/' + 'ref'
  resdir = tempfile.gettempdir()
  __main__.main([ '--src-dir', srcdir, '--dst-dir', resdir, '--force' ])

  # this is not possible to compare binary files because of ffmpeg version
  # which is not constant over time and os
  check_file(refdir, resdir, 'timer.mp4', 'mp4')

def test_animated():
  """
  Test of a mp4 transformed in animated gif and webp
  """
  srcdir = 'tests/data/mp4'
  refdir = srcdir + '/' + 'ref'
  resdir = tempfile.gettempdir()
  __main__.main([ '--src-dir', srcdir, '--dst-dir', resdir, '--mp4-as-gif', '--force' ])

  # this is not possible to compare binary files because of ffmpeg version
  # which is not constant over time and os
  check_file(refdir, resdir, 'timer.gif', 'gif')
  check_file(refdir, resdir, 'timer.webp', 'webp')
