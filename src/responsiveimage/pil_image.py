'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import os
from PIL import Image, ImageOps    # python -m pip install --upgrade pillow

from . import argsResponsiveImage
from . import exif as getexif
from . import webp
from . import png
from . import jpg

def responsive(args: argsResponsiveImage.argsResponsiveImage, filename: str, filetype: str):
  args.inc()
  srcFullFilename = os.path.join(args.args.src_dir, filename)
  dstFullFilename = os.path.join(args.args.dst_dir, filename)
  if os.path.isfile(dstFullFilename):
    args.print(filename, False)
    return

  args.print(filename, True)
  image_org = Image.open(srcFullFilename)

  # from https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
  if (args.args.rotate):
    image_org = ImageOps.exif_transpose(image_org)
  exif, epoch = getexif.getExif(image_org, srcFullFilename, filetype)

  width = image_org.width
  height = image_org.height
  max_size = max(width, height)

  sizes = args.args.size.split(',')
  for size in sizes:
    f = int(size) / max_size
    if (f < 1):
      image = image_org.resize((int(width * f), int(height * f)))
    else:
      image = image_org

    if filetype == 'jpg':
      jpg.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)
    elif filetype == 'webp':
      webp.save(image, srcFullFilename, dstFullFilename, epoch, args)
    elif filetype == 'png':
      # TODO: optipng call too
      png.save(image, srcFullFilename, dstFullFilename, exif, epoch, args)

    if filetype!='webp' and args.args.export_to_webp:
      (name, _) = os.path.splitext(dstFullFilename)
      dstFullFilename = name + '.webp'
      webp.save(image, srcFullFilename, dstFullFilename, epoch, args)

# TODO: noRafale
#       if (args.noRafale) and (epoch!=0) and (epoch-last_epoch < args.noRafale) and (epoch>=last_epoch):
#         print('Skip as date acquisition too close')
#         last_epoch = epoch
#         continue

#       last_epoch = epoch
