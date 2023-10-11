'''
MIT License
Copyright (c) 2023 Pascal Brand

create responsive images, based on list of sizes
'''

import os
from PIL import Image     # python -m pip install --upgrade pillow
# from PIL import ImageOps

from . import argsResponsiveImage
from . import exif as getexif
from . import webp
from . import png
from . import jpg

def missingOutput(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str):
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

def transform(image_org, value, what):
  '''
  Transform original image
  '''
  if what == 0:
    f = int(value) / max(image_org.width, image_org.height)
  else:
    f = int(value) / image_org.height
  if (f < 1):
    return image_org.resize((int(image_org.width * f), int(image_org.height * f)))
  else:
    return image_org

def responsive(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str):
  '''
  create responsive version of the images
  '''
  args.inc()
  if (not args.args.force) and (not missingOutput(args, filename, filetype)):
    args.print(filename, False)
    return
  args.print(filename, True)

  srcFullFilename = os.path.join(args.args.src_dir, filename)
  image_org = Image.open(srcFullFilename)

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
    image = transform(image_org, transforms[index], what)

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

  _hack(image_org, filename, args, exif, epoch, filetype)


# TODO: noRafale
#       if (args.noRafale) and (epoch!=0) and (epoch-last_epoch < args.noRafale) and (epoch>=last_epoch):
#         print('Skip as date acquisition too close')
#         last_epoch = epoch
#         continue

#       last_epoch = epoch


# TODO: make it generic
# used for slides image:
# - slide aspect-ratio on screen > 512px:  1/4, that is width=1024 and height=256
# - slide aspect-ratio on screen >= 512px: 2/5, that is width=512 and height=205 ==> crop can be performed
# 256 height

def _hack(image_org, filename, args, exif, epoch, filetype):
  '''
  hack to crop images in special case for slides
  TODO: make this hack clean

  - slide aspect-ratio on screen > 512px:  1/4, that is width=1024 and height=256
  - slide aspect-ratio on screen >= 512px: 2/5, that is width=512 and height=205
    ==> crop can be performed 256 height
  '''
  width = image_org.width
  height = image_org.height
  srcFullFilename = os.path.join(args.args.src_dir, filename)

  if (filetype == 'jpg') and (height == 256):   # this is a slide image
    (srcName, _) = os.path.splitext(filename)

    image = image_org
    dstFullFilename = os.path.join(args.args.dst_dir, srcName + '-h256.jpg')
    jpg.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)

    dstFullFilename = os.path.join(args.args.dst_dir, srcName + '-h256.webp')
    webp.save(image, srcFullFilename, dstFullFilename, epoch, args)

    if (width == 1024):
      width = height * 5/2
      image = image.crop((0, 0, width, height))

    # image for slides on small screen (max 512px wide)
    f = (512 * 2/5) / height
    image = image.resize((int(width * f), int(height * f)))

    dstFullFilename = os.path.join(args.args.dst_dir, srcName + '-hsmall.jpg')
    jpg.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)

    dstFullFilename = os.path.join(args.args.dst_dir, srcName + '-hsmall.webp')
    webp.save(image, srcFullFilename, dstFullFilename, epoch, args)
