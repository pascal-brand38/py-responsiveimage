'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import os
import shutil
import filecmp
from . import argsResponsiveImage

def _copy_file(filename_src:str, filename_dst:str):
  # as we check whether the files are the same or not, no need to force
  if (not os.path.isfile(filename_dst) or (not filecmp.cmp(filename_src, filename_dst))):
    try:
      shutil.copy2(filename_src, filename_dst)
    except:
      print('   === cannot copy ' + filename_src + ' to ' + filename_dst)


def responsive(args: argsResponsiveImage.argsResponsiveImage, filename):
  args.inc()
  if os.path.isfile(os.path.join(args.args.dst_dir, filename)):
    args.print(filename, False)
    return

  args.print(filename, True)
  _copy_file(os.path.join(args.args.src_dir, filename), os.path.join(args.args.dst_dir, filename))
