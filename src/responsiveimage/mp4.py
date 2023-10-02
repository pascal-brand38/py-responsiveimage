'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import os
import shutil
import subprocess
from . import argsResponsiveImage

def responsive(args: argsResponsiveImage.argsResponsiveImage, filename):
  args.inc()
  srcFullFilename = os.path.join(args.args.src_dir, filename)
  dstFullFilename = os.path.join(args.args.dst_dir, filename)
  if os.path.isfile(dstFullFilename):
    args.print(filename, False)
    return

  args.print(filename, True)
  subprocess.call([
    'ffmpeg',
    '-i', srcFullFilename,
    '-map_metadata', '0',   # copy video media properties - keep this option right after the -i option
    '-vf', 'scale=1024:-1',
    dstFullFilename,
    '-loglevel', 'quiet'
    ])

  # update timestamp
  shutil.copystat(srcFullFilename, dstFullFilename)
