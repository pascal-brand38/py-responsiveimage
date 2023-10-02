'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

import argparse
import os
import filetype
from . import gif
from . import jpg
from . import png
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
  return parser


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
    elif (kind.extension == 'jpg'):
      jpg.responsive(args, filename)
    elif (kind.extension == 'png'):
      png.responsive(args, filename)
    elif (kind.extension == 'mp4'):
      mp4.responsive(args, filename)
    else:
      print('File type ' + kind.extension + ' not supported - file ' + filename)

if __name__ == "__main__":
  main()
