'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import os
import shutil
from PIL import Image, ImageOps    # python -m pip install --upgrade pillow

from . import argsResponsiveImage
from . import exif as getexif


# TODO: lots of common code with jpg
def responsive(args: argsResponsiveImage.argsResponsiveImage, filename):
  args.inc()
  srcFullFilename = os.path.join(args.args.src_dir, filename)
  dstFullFilename = os.path.join(args.args.dst_dir, filename)
  if os.path.isfile(dstFullFilename):
    args.print(filename, False)
    return

  args.print(filename, True)
  image = Image.open(srcFullFilename)

  # from https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
  if (args.args.rotate):
    image = ImageOps.exif_transpose(image)

  exif, epoch = getexif.getExif(image, srcFullFilename, 'jpg')

  width = image.width
  height = image.height
  if width > height:
    f = 1920 / width    # TODO
  else:
    f = 1920 / height

  if (f < 1):
    try:
      image = image.resize((int(width * f), int(height * f)))
    except:
      print('NO WAY for resizing ' + filename)
      return

  if exif:
    image.save(dstFullFilename, optimize=True, exif=exif)
  else:
    image.save(dstFullFilename, optimize=True)

  # TODO: optipng call too

  # update timestamp
  shutil.copystat(srcFullFilename, dstFullFilename)
  if (epoch != 0):
    os.utime(dstFullFilename, (epoch, epoch))
