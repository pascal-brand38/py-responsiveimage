'''
MIT License
Copyright (c) 2023 Pascal Brand

jpg utility functions:
- save
'''

from . import argsResponsiveImage
from . import exif as getexif

def save(image, srcFullFilename, dstFullFilename, exif, epoch, args: argsResponsiveImage.argsResponsiveImage):
  '''
  save image as jpg format, as name dstFullFilename
  - use exif is not None
  - args is used to get webp parameters, as args.parameters['webp']
  - srcFullFilename and epoch are used to keep modification dates
  '''
  parameters = args.parameters['jpg']
  if exif:
    image.save(dstFullFilename, quality=parameters['quality'], progressive=parameters['progressive'], optimize=True, subsampling=parameters['subsampling'], exif=exif)
  else:
    image.save(dstFullFilename, quality=parameters['quality'], progressive=parameters['progressive'], optimize=True, subsampling=parameters['subsampling'])
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
