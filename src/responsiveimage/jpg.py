'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

from . import argsResponsiveImage
from . import exif as getexif

def save(image, srcFullFilename, dstFullFilename, exif, epoch, args: argsResponsiveImage.argsResponsiveImage):
  parameters = args.parameters['jpg']
  if exif:
    image.save(dstFullFilename, quality=parameters['quality'], progressive=parameters['progressive'], optimize=True, subsampling=parameters['subsampling'], exif=exif)
  else:
    image.save(dstFullFilename, quality=parameters['quality'], progressive=parameters['progressive'], optimize=True, subsampling=parameters['subsampling'])
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
