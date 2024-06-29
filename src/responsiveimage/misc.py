'''
MIT License
Copyright (c) Pascal Brand

create responsive images, based on list of sizes
'''

import os
from . import argsResponsiveImage

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
