'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
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
  parser.add_argument('--size',
                      help='TODO',
                      required=False,
                      default='1920')
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
  return parser


def main(cmdargs):
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
    if (extension == 'jpg') or (extension == 'png') or (extension == 'webp'):
      pil_image.responsive(args, filename, extension)
    elif (extension == 'mp4'):
      mp4.responsive(args, filename)
    elif (extension == 'gif') or (extension == 'svg'):
      copy_image.responsive(args, filename, extension)
    else:
      print('File extension ' + extension + ' not supported - file ' + filename)

if __name__ == "__main__":
  main(sys.argv[1:])
