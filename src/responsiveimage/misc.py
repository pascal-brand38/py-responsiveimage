'''
MIT License
Copyright (c) Pascal Brand

create responsive images, based on list of sizes
'''

import os
from . import argsResponsiveImage
from . import exif as getexif
from PIL import Image
from time import strftime, localtime
import re

def missingOutput(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str) -> bool:
  '''
  return True if one of the output is missing
  In that case, further processing is skipped
  '''
  adds = args.args.add_name.split(',')
  (srcName, srcExt) = os.path.splitext(filename)
  for add in adds:
    if (not os.path.isfile(os.path.join(args.args.dst_dir, srcName + add + srcExt))) and (not os.path.isfile(os.path.join(args.args.dst_dir, srcName + add + '.' + filetype))):
      return True
    if filetype!='webp' and args.args.export_to_webp:
      if not os.path.isfile(os.path.join(args.args.dst_dir, srcName + add + '.webp')):
        return True
  return False


def getDstFilename(args: argsResponsiveImage.argsResponsiveImage, srcFilename: str, filetype: str, image: Image.Image) -> bool:
  if not(args.args.rename):
    return srcFilename

  dstFilename = srcFilename
  (srcName, srcExt) = os.path.splitext(srcFilename)
  dirName = os.path.dirname(srcFilename)
  if re.match(r'^[0-9]{8}_[0-9]{6}$', srcName):     # the acquisition date followed by the time
    # no rename as already the correct filename
    return srcFilename

  srcFullFilename = os.path.join(args.args.src_dir, srcFilename)
  exif, epoch = getexif.getExif(image, srcFullFilename, filetype)

  if (epoch != 0):
    # dst srcFilename is renamed using the date of the file
    dstFilename = os.path.join(dirName, strftime('%Y%m%d_%H%M%S', localtime(epoch)) + srcExt)

  # print(srcFilename, ' ==> ', dstFilename)
  return dstFilename
