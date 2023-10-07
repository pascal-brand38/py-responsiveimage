'''
MIT License
Copyright (c) 2023 Pascal Brand

webp utility functions:
- save
'''

from . import argsResponsiveImage
from . import exif as getexif

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
# method=6 provides a better size, but is slow
def save(image, srcFullFilename, dstFullFilename, epoch, args: argsResponsiveImage.argsResponsiveImage):
  '''
  save image as webp format, as name dstFullFilename
  - args is used to get webp parameters, as args.parameters['webp']
  - srcFullFilename and epoch are used to keep modification dates
  '''
  parameters = args.parameters['webp']
  image.save(dstFullFilename, method=6, quality=parameters['quality'])
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
