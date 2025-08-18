'''
MIT License
Copyright (c) 2023 Pascal Brand

bare-copy of the file
'''

import os
import shutil
import filecmp
from PIL import Image   # python -m pip install --upgrade pillow
from . import argsResponsiveImage
from . import misc
from . import exif as getexif

def _copy_file(filename_src:str, filename_dst:str) -> None:
  '''
  copy the file filename_src to filename_dst (full file name)
  '''
  # as we check whether the files are the same or not, no need to force
  if (not os.path.isfile(filename_dst) or (not filecmp.cmp(filename_src, filename_dst))):
    try:
      shutil.copy2(filename_src, filename_dst)
    except:
      print('   === cannot copy ' + filename_src + ' to ' + filename_dst)


def responsive(args: argsResponsiveImage.argsResponsiveImage, filename, filetype: str, nb: int) -> None:
  '''
  get the responsive version of the image by copying it only
  used for gif and svg
  '''
  srcFullFilename = os.path.join(args.args.src_dir, filename)
  # try-catch as svg cannot be opened
  try:
    image = Image.open(srcFullFilename)
  except:
    image = None
  dstFilename = misc.getDstFilename(args, filename, filetype, image)
  dstFullFilename = os.path.join(args.args.dst_dir, dstFilename)

  if (not args.args.force) and (os.path.isfile(dstFullFilename)):
    args.print(filename, False, nb)
    return

  args.print(filename, True, nb)
  _copy_file(srcFullFilename, dstFullFilename)

  # update stats info on the image from exif if possible
  if (image is not None):
    _, epoch = getexif.getExif(image, srcFullFilename, filetype)
    getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
