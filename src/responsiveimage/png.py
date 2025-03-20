'''
MIT License
Copyright (c) 2023 Pascal Brand

webp utility functions:
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
  save image as png format, as name dstFullFilename
  - use exif is not None
  - srcFullFilename and epoch are used to keep modification dates
  '''
  if exif:
    image.save(dstFullFilename, optimize=True, format='PNG', exif=exif)
  else:
    image.save(dstFullFilename, optimize=True, format='PNG')
  getexif.updateFilestat(srcFullFilename, dstFullFilename, epoch)
