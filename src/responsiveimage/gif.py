'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import os
import shutil
import filecmp
from . import argsResponsiveImages

def _copy_file(filename_src:str, filename_dst:str):
  # as we check whether the files are the same or not, no need to force
  if (not os.path.isfile(filename_dst) or (not filecmp.cmp(filename_src, filename_dst))):
    try:
      shutil.copy2(filename_src, filename_dst)
    except:
      print('   === cannot copy ' + filename_src + ' to ' + filename_dst)

def responsive(args: argsResponsiveImages.argsResponsiveImages, filename):
  args.inc()
  if os.path.isfile(args.args.dst_dir + '/' + filename):
    args.print(filename, False)
  else:
    args.print(filename, True)
    _copy_file(args.args.src_dir + '/' + filename, args.args.dst_dir + '/' + filename)
