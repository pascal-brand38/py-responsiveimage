'''
MIT License
Copyright (c) 2023 Pascal Brand

jpg utility functions:
- save
'''

from typing import Union
from PIL import Image
from . import argsResponsiveImage
from . import exif as getexif

def save(
    image:Image.Image,
    srcFullFilename:str,
    dstFullFilename:str,
    exif: Union[Image.Exif, None],
    epoch:float,
    args: argsResponsiveImage.argsResponsiveImage) -> None:
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
