'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import argparse
import os
import sys
import filetype
from . import webp
from . import copy_image
from . import pil_image
from . import mp4
from . import argsResponsiveImage

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
  parser.add_argument('--export-to-webp',
                      help='png and jpg are exported in webp format too',
                      required=False,
                      default=False,
                      action='store_true')
  return parser


def main(cmdargs):
  parser = _createParser()
  args = argsResponsiveImage.argsResponsiveImage(parser.parse_args(cmdargs), 0)

  if not os.path.isdir(args.args.dst_dir):
    os.mkdir(args.args.dst_dir)

  for filename in os.listdir(args.args.src_dir):
    kind = filetype.guess(args.args.src_dir + '/' + filename)
    if kind is None:
      continue

    # See kind.EXTENSION for supported extensions
    if (kind.extension == 'jpg') or (kind.extension == 'png') or (kind.extension == 'webp'):
      pil_image.responsive(args, filename, kind.extension)
    elif (kind.extension == 'mp4'):
      mp4.responsive(args, filename)
    elif (kind.extension == 'gif') or (filename.endswith('.svg')):
      copy_image.responsive(args, filename, kind.extension)
    else:
      print('File type ' + kind.extension + ' not supported - file ' + filename)

if __name__ == "__main__":
  main(sys.argv[1:])
