'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

from . import argsResponsiveImage
from . import exif as getexif

def save(image, srcFullFilename, dstFullFilename, exif, epoch, args: argsResponsiveImage.argsResponsiveImage):
  if exif:
    image.save(dstFullFilename, optimize=True, exif=exif)
  else:
    image.save(dstFullFilename, optimize=True)
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
