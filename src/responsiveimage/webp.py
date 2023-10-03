'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

from . import argsResponsiveImage
from . import exif as getexif

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
# method=6 provides a better size, but is slow
def save(image, srcFullFilename, dstFullFilename, epoch, args: argsResponsiveImage.argsResponsiveImage):
  parameters = args.parameters['webp']
  image.save(dstFullFilename, method=6, quality=parameters['quality'])
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
