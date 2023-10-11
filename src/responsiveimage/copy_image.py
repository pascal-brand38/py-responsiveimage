'''
MIT License
Copyright (c) 2023 Pascal Brand

bare-copy of the file
'''

import os
import shutil
import filecmp
from . import argsResponsiveImage

def _copy_file(filename_src:str, filename_dst:str):
  '''
  copy the file filename_src to filename_dst (full file name)
  '''
  # as we check whether the files are the same or not, no need to force
  if (not os.path.isfile(filename_dst) or (not filecmp.cmp(filename_src, filename_dst))):
    try:
      shutil.copy2(filename_src, filename_dst)
    except:
      print('   === cannot copy ' + filename_src + ' to ' + filename_dst)


def responsive(args: argsResponsiveImage.argsResponsiveImage, filename, filetype: str):
  '''
  get the responsive version of the image by copying it only
  used for gif and svg
  '''
  args.inc()
  if (not args.args.force) and (os.path.isfile(os.path.join(args.args.dst_dir, filename))):
    args.print(filename, False)
    return

  args.print(filename, True)
  _copy_file(os.path.join(args.args.src_dir, filename), os.path.join(args.args.dst_dir, filename))
