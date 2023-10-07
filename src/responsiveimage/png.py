'''
MIT License
Copyright (c) 2023 Pascal Brand

webp utility functions:
- save
'''

from . import argsResponsiveImage
from . import exif as getexif

def save(image, srcFullFilename, dstFullFilename, exif, epoch, args: argsResponsiveImage.argsResponsiveImage):
  '''
  save image as png format, as name dstFullFilename
  - use exif is not None
  - args is used to get webp parameters, as args.parameters['webp']
  - srcFullFilename and epoch are used to keep modification dates
  '''
  if exif:
    image.save(dstFullFilename, optimize=True, exif=exif)
  else:
    image.save(dstFullFilename, optimize=True)
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
