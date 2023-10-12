'''
MIT License
Copyright (c) 2023 Pascal Brand

mp4 utility functions:
- save
'''

import os
import shutil
import subprocess
import tempfile
from . import argsResponsiveImage

def responsive(args: argsResponsiveImage.argsResponsiveImage, filename):
  '''
  process mp4 file filename (only the filename, without src_dir)

  if args.args.mp4_as_gif:
  - create animated gif and webp

  otherwise
  - rescale mp4 (TODO: right now 1024)
  '''

  args.inc()

  srcFullFilename = os.path.join(args.args.src_dir, filename)
  dstFullFilename = os.path.join(args.args.dst_dir, filename)

  if args.args.mp4_as_gif:
    (dstName, _) = os.path.splitext(dstFullFilename)

    filename_gif = dstName +'.gif'
    filename_webp = dstName +'.webp'

    if (not args.args.force) and (os.path.isfile(filename_gif)) and (os.path.isfile(filename_webp)):
      args.print(filename, False)
      return

    args.print(filename, True)

    # mp4 -> gif: https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
    palette = tempfile.gettempdir() + '/palette.png'
    filters='fps=2,scale=-1:-1:flags=lanczos'

    subprocess.call([
      'ffmpeg',
      '-y',
      '-i', srcFullFilename,
      '-vf', filters+',palettegen',
      '-y', palette ])

    subprocess.call([
      'ffmpeg',
      '-y',
      '-i', srcFullFilename,
      '-i', palette,
      '-lavfi', filters + ' [x]; [x][1:v] paletteuse',
      '-y',
      '-loop', '0',
      '-compression_level', '6',
      filename_gif])

    # mp4 -> webp
    subprocess.call([
      'ffmpeg',
      '-y',
      '-i', srcFullFilename,
      '-i', palette,
      '-lavfi', filters + ' [x]; [x][1:v] paletteuse',
      '-y',
      '-loop', '0',
      '-compression_level', '6',
      filename_webp])

  else:

    if (not args.args.force) and (os.path.isfile(dstFullFilename)):
      args.print(filename, False)
      return

    args.print(filename, True)
    subprocess.call([
      'ffmpeg',
      '-y',
      '-i', srcFullFilename,
      '-map_metadata', '0',   # copy video media properties - keep this option right after the -i option
      '-vf', 'scale=1024:-1',   # todo: scale
      dstFullFilename,
      '-loglevel', 'quiet'
      ])

    # update timestamp
    shutil.copystat(srcFullFilename, dstFullFilename)
