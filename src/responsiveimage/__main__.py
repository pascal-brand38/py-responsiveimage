'''
MIT License
Copyright (c) 2023 Pascal Brand

Main function of responsiveimage package
'''

import argparse
import os
import sys
import filetype
from . import copy_image
from . import pil_image
from . import mp4
from . import argsResponsiveImage

def _createParser():
  '''
  parse commandline options
  '''
  parser = argparse.ArgumentParser(
     prog='responsiveimage',
     description='Create different image versions (size, quality, format) from original images',
     formatter_class=argparse.RawTextHelpFormatter
     )

  # parser.add_argument('--rotate',
  #                     help='',
  #                     required=False,
  #                     default=False,
  #                     action='store_true')
  # parser.add_argument('--no-rafale',
  #                     help='',
  #                     required=False,
  #                     default=False,
  #                     action='store_true')
  parser.add_argument('--src-dir',
                      help='source directory. Default: /tmp/toreduce',
                      required=False,
                      default='/tmp/toreduce')
  parser.add_argument('--dst-dir',
                      help='destination directory. Default: /tmp/reduced',
                      required=False,
                      default='/tmp/reduced')
  parser.add_argument('--size',
                      help='list of sizes, separated by commas, of different scale. Ex: 1024,512. Default: 1920px if --height not set',
                      required=False,
                      default=None)
  parser.add_argument('--height',
                      help='list of heights, separated by commas, of different scale. Ex: 1024,512. Cannot be used when --size',
                      required=False,
                      default=None)
  parser.add_argument('--export-to-webp',
                      help='png and jpg are exported in webp format too',
                      required=False,
                      default=False,
                      action='store_true')
  parser.add_argument('--mp4-as-gif',
                      help='mp4 saved as .gif and .webo',
                      required=False,
                      default=False,
                      action='store_true')
  parser.add_argument('--add-name',
                      help='list of added name. Default is nothing when a single transform, or size otherwise',
                      required=False,
                      default=None)
  parser.add_argument('--crop',
                      help='x1,y1,x2,y2: crop the original image before rescaling',
                      required=False,
                      default=None)
  parser.add_argument('--force',
                      help='rewrite files',
                      required=False,
                      default=False,
                      action='store_true')

  return parser


def main(cmdargs):
  '''
  main function of python package responsiveimage
  '''
  parser = _createParser()
  args = argsResponsiveImage.argsResponsiveImage(parser.parse_args(cmdargs), 0)

  if not os.path.isdir(args.args.dst_dir):
    os.mkdir(args.args.dst_dir)

  for filename in os.listdir(args.args.src_dir):
    if not os.path.isfile(os.path.join(args.args.src_dir, filename)):
      print('Skip directory ' + filename)
      continue

    kind = filetype.guess(args.args.src_dir + '/' + filename)
    if kind is None:
      (_, extension) = os.path.splitext(filename)
      if extension != '':
        extension = extension[1:].lower()
    else:
      extension = kind.extension


    # See kind.EXTENSION for supported extensions
    if extension in [ 'jpg', 'png', 'webp' ]:
      pil_image.responsive(args, filename, extension)
    elif extension in [ 'mp4' ]:
      mp4.responsive(args, filename)
    elif extension in [ 'gif', 'svg' ]:
      copy_image.responsive(args, filename, extension)
    else:
      print('File extension ' + extension + ' not supported - file ' + filename)

if __name__ == "__main__":
  main(sys.argv[1:])
