'''
MIT License
Copyright (c) 2023 Pascal Brand

create responsive images, based on list of sizes
'''

import os
from typing import List, Union
from PIL import Image     # python -m pip install --upgrade pillow
# from PIL import ImageOps

from . import argsResponsiveImage
from . import exif as getexif
from . import webp
from . import png
from . import jpg

def missingOutput(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str) -> bool:
  '''
  return True if one of the output is missing
  In that case, further processing is skipped
  '''
  adds = args.args.add_name.split(',')
  (srcName, srcExt) = os.path.splitext(filename)
  for add in adds:
    if not os.path.isfile(os.path.join(args.args.dst_dir, srcName + add + srcExt)):
      return True
    if filetype!='webp' and args.args.export_to_webp:
      if not os.path.isfile(os.path.join(args.args.dst_dir, srcName + add + '.webp')):
        return True
  return False

def resize(image_org: Image.Image, value: str, what: int) -> Image.Image:
  '''
  Transform original image, value being, depending on what:
  - what==0 ==> value == max size
  - what==1 ==> value == height
  '''
  if what == 0:
    f = float(value) / max(image_org.width, image_org.height)
  else:
    f = float(value) / image_org.height
  if (f < 1):
    return image_org.resize((int(image_org.width * f), int(image_org.height * f)))
  else:
    return image_org


def crop(image_org:Image.Image, values: Union[None, List[int]]) -> Image.Image:
  '''
  Crop image
  '''
  if values is None:
    return image_org

  if (values[0] > image_org.width):
    return image_org
  if (values[2] > image_org.width):
    return image_org

  if (values[1] > image_org.height):
    return image_org
  if (values[3] > image_org.height):
    return image_org

  return image_org.crop((values[0], values[1], values[2], values[3]))



def responsive(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str, nb: int) -> None:
  '''
  create responsive version of the images
  '''
  if (not args.args.force) and (not missingOutput(args, filename, filetype)):
    args.print(filename, False, nb)
    return
  args.print(filename, True, nb)

  srcFullFilename = os.path.join(args.args.src_dir, filename)
  image_org = Image.open(srcFullFilename)
  image_org = crop(image_org, args.args.crop)

  (srcName, srcExt) = os.path.splitext(filename)

  adds = args.args.add_name.split(',')
  if args.args.size is not None:
    transforms = args.args.size.split(',')
    what = 0
  else:
    transforms = args.args.height.split(',')
    what = 1

  # from https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
  # if (args.args.rotate):
  #   image_org = ImageOps.exif_transpose(image_org)
  exif, epoch = getexif.getExif(image_org, srcFullFilename, filetype)

  for index, _ in enumerate(adds):
    dstFullFilename = os.path.join(args.args.dst_dir, srcName + adds[index] + srcExt)
    image = resize(image_org, transforms[index], what)

    if filetype == 'jpg':
      jpg.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)
    elif filetype == 'webp':
      webp.save(image, srcFullFilename, dstFullFilename, epoch, args)
    elif filetype == 'png':
      # TODO: optipng call too
      png.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)

    if filetype!='webp' and args.args.export_to_webp:
      dstFullFilename = os.path.join(args.args.dst_dir, srcName + adds[index] + '.webp')
      webp.save(image, srcFullFilename, dstFullFilename, epoch, args)

#       if (args.noRafale) and (epoch!=0) and (epoch-last_epoch < args.noRafale) and (epoch>=last_epoch):
#         print('Skip as date acquisition too close')
#         last_epoch = epoch
#         continue
#       last_epoch = epoch
