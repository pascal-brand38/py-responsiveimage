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
from . import misc

def responsive(args: argsResponsiveImage.argsResponsiveImage, filename: str, nb: int) -> None:
  '''
  process mp4 file filename (only the filename, without src_dir)

  if args.args.mp4_as_gif:
  - create animated gif and webp

  otherwise
  - rescale mp4 (TODO: right now 1024)
  '''

  srcFullFilename = os.path.join(args.args.src_dir, filename)
  dstFullFilename = os.path.join(args.args.dst_dir, filename)

  if args.args.mp4_as_gif:
    if (not args.args.force) and (not misc.missingOutput(args, filename, 'gif')):
      args.print(filename, False, nb)
      return
    args.print(filename, True, nb)

    (srcName, _) = os.path.splitext(filename)

    adds = args.args.add_name.split(',')
    if args.args.size is not None:
      transforms = args.args.size.split(',')
      what = 0
    else:
      transforms = args.args.height.split(',')
      what = 1

    for index, _ in enumerate(adds):
      filename_gif = os.path.join(args.args.dst_dir, srcName + adds[index] + '.gif')
      filename_webp = os.path.join(args.args.dst_dir, srcName + adds[index] + '.webp')
      # image = resize(image_org, transforms[index], what)
      # scale = "scale=w=" + transforms[index] + ":h=" + transforms[index] + ":force_original_aspect_ratio=decrease"
      scale = "scale=w='min(" + transforms[index] + ",iw)':h='min(" + transforms[index] + ",ih)':force_original_aspect_ratio=decrease"

      # mp4 -> gif: https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
      palette = tempfile.gettempdir() + '/palette.png'
      filters='fps=2,' + scale + ':flags=lanczos'

      subprocess.call([
        'ffmpeg',
        '-i', srcFullFilename,
        '-vf', filters+',palettegen',
        '-y',
        '-loglevel', 'error',
        palette ])

      subprocess.call([
        'ffmpeg',
        '-y',
        '-i', srcFullFilename,
        '-i', palette,
        '-lavfi', filters + ' [x]; [x][1:v] paletteuse',
        '-y',
        '-loop', '0',
        '-compression_level', '6',
        '-loglevel', 'error',
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
        '-loglevel', 'error',
        filename_webp])

  else:

    if (not args.args.force) and (os.path.isfile(dstFullFilename)):
      args.print(filename, False, nb)
      return
    args.print(filename, True, nb)

    # -vf option: https://trac.ffmpeg.org/wiki/Scaling
    # pad: cf. https://stackoverflow.com/questions/20847674/ffmpeg-libx264-height-not-divisible-by-2
    subprocess.call([
      'ffmpeg',
      '-y',
      '-i', srcFullFilename,
      '-map_metadata', '0',   # copy video media properties - keep this option right after the -i option
      '-vf', 'scale=w=\'min(1024,iw)\':h=\'min(1024,ih)\':force_original_aspect_ratio=decrease,pad=ceil(iw/2)*2:ceil(ih/2)*2',   # todo: scale
      '-vcodec', 'libx264',     # https://stackoverflow.com/questions/3561715/using-ffmpeg-to-encode-a-high-quality-video
      '-crf', '18',
      '-preset', 'veryslow',
      dstFullFilename,
      '-loglevel', 'error',
      # '-loglevel', 'quiet'
      ])

    # update timestamp
    shutil.copystat(srcFullFilename, dstFullFilename)
