'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import argparse
import os
import filecmp
import shutil, subprocess
from datetime import datetime
import json
import filetype
from . import gif
from . import argsResponsiveImage

# python -m pip install --upgrade pillow
from PIL import Image, ImageOps, ExifTags

def _createParser():
  parser = argparse.ArgumentParser(
     prog='responsiveimage',
     description='Create different image versions (size, quality, format) from original images',
     formatter_class=argparse.RawTextHelpFormatter
     )

  parser.add_argument('--rotate',
                      help='TODO',
                      required=False,
                      default=False,
                      action='store_true')
  parser.add_argument('--no-rafale',
                      help='TODO',
                      required=False,
                      default=False,
                      action='store_true')
  parser.add_argument('--src-dir',
                      help='TODO',
                      required=False,
                      default='/tmp/toreduce')
  parser.add_argument('--dst-dir',
                      help='TODO',
                      required=False,
                      default='/tmp/reduced')
  return parser


def printExifTags(exif):
  info = None
  for key, val in exif.items():
    if key in ExifTags.TAGS:
      print(f'{key}:{ExifTags.TAGS[key]}:{val}')
      if ExifTags.TAGS[key] == "ExifOffset":   # from https://github.com/python-pillow/Pillow/issues/5863
        info = exif.get_ifd(key)
  if info:
    for key, val in info.items():
      if key in ExifTags.TAGS:
        print(f'{key}:{ExifTags.TAGS[key]}:{val}')


def main():
  parser = _createParser()
  args = argsResponsiveImage.argsResponsiveImage(parser.parse_args(), 0)

  if not os.path.isdir(args.args.dst_dir):
    os.mkdir(args.args.dst_dir)

  nb = 0
  last_epoch = 0
  for filename in os.listdir(args.args.src_dir):
    kind = filetype.guess(args.args.src_dir + '/' + filename)
    if kind is None:
      continue

    # See kind.EXTENSION for supported extensions
    if (kind.extension == 'gif'):
      gif.responsive(args, filename)
    else:
      print('File type ' + kind.extension + ' not supported - file ' + filename)

  #   isJpg = (filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.JPEG'))
  #   isPng = (filename.endswith('.png') or filename.endswith('.PNG'))
  #   isGif = (filename.endswith('.gif') or filename.endswith('.GIF'))
  #   if isPng or isJpg:
  #       nb = nb + 1
  #       if os.path.isfile(_dirresized + '/' + filename):
  #         print('  - ' + str(nb) + ' ' + filename)
  #         continue
  #       print('  + ' + str(nb) + ' ' + filename)
  #       try:
  #         image = Image.open(_dirimg + '/' + filename)
  #         if (isPng):
  #           image.load()      # https://stackoverflow.com/questions/48631908/python-extract-metadata-from-png
  #       except:
  #         print('NO WAY to open ' + filename)
  #         continue
  #       width = image.width
  #       height = image.height
  #       if width > height:
  #         f = 1920 / width
  #       else:
  #         f = 1920 / height

  #       try:
  #         noexif = False
  #         exif = image.getexif()
  #         # printExifTags(exif)
  #         # 34665===ExifOffset  and  36867===DateTimeOriginal
  #         info = exif.get_ifd(34665)
  #         dateTimeOriginal = None
  #         if (info):
  #           dateTimeOriginal = info.get(36867)
  #         if not dateTimeOriginal and isPng:
  #           dateTimeOriginal = image.info.get('Creation Time')

  #         if not dateTimeOriginal:
  #           # no acquisition date in exif nor png metadata
  #           # check if a json file exist (from a google photo for example)
  #           try:
  #             with open(_dirimg + '/' + filename + '.json') as json_file:
  #               jsonData = json.load(json_file)
  #               epoch = int(jsonData['photoTakenTime']['timestamp'])
  #               dateTimeOriginal = datetime.fromtimestamp(epoch).strftime('%Y:%m:%d %H:%M:%S')
  #           except:
  #             pass



  #         if dateTimeOriginal:
  #           # set in exif + png metadata
  #           if info:
  #             info[36867] = dateTimeOriginal
  #           epoch = datetime.strptime(dateTimeOriginal, '%Y:%m:%d %H:%M:%S').timestamp()
  #         else:
  #           epoch = 0

  #       except:
  #         print('  no exif in ' + filename)
  #         noexif = True
  #         epoch = 0

  #       if (args.noRafale) and (epoch!=0) and (epoch-last_epoch < args.noRafale) and (epoch>=last_epoch):
  #         print('Skip as date acquisition too close')
  #         last_epoch = epoch
  #         continue

  #       last_epoch = epoch

  #       if (f < 1):
  #         try:
  #           image = image.resize((int(width * f), int(height * f)))
  #         except:
  #           print('NO WAY for resizing ' + filename)
  #           continue

  #       # from https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
  #       if (args.rotate):
  #         image = ImageOps.exif_transpose(image)

  #       if (noexif):
  #         if (isPng):
  #           image.save(_dirresized + '/' + filename, optimize=True)
  #         if (isJpg):
  #           image.save(_dirresized + '/' + filename, quality=80, progressive=True, optimize=True, subsampling='4:2:0')
  #       else:
  #         if (isPng):
  #           image.save(_dirresized + '/' + filename, optimize=True, exif=exif)
  #         if (isJpg):
  #           image.save(_dirresized + '/' + filename, quality=80, progressive=True, optimize=True, subsampling='4:2:0', exif=exif)

  #       # update timestamp
  #       shutil.copystat(_dirimg + '/' + filename, _dirresized + '/' + filename)
  #       #os.stat(_dirresized + '/' + filename).st_ctime(dateTimeOriginal)
  #       if (epoch != 0):
  #         os.utime(_dirresized + '/' + filename, (epoch, epoch))

  # # resize video too
  # for mp4_filename in os.listdir(_dirimg):
  #   if mp4_filename.endswith('.mp4') or mp4_filename.endswith('.MP4'):
  #     nb = nb + 1
  #     if os.path.isfile(_dirresized + '/' + mp4_filename):
  #       print('  - ' + str(nb) + ' ' + mp4_filename)
  #       continue
  #     print('  + ' + str(nb) + ' ' + mp4_filename)
  #     subprocess.call([
  #       'ffmpeg',
  #       '-i', _dirimg + '/'+mp4_filename,
  #       '-map_metadata', '0',   # copy video media properties - keep this option right after the -i option
  #       '-vf', 'scale=1024:-1',
  #       _dirresized + '/' + mp4_filename,
  #       '-loglevel', 'quiet'
  #       ])
  #     # update timestamp
  #     # shutil.copystat(_dirimg + '/' + mp4_filename, _dirresized + '/' + mp4_filename)

if __name__ == "__main__":
  main()
