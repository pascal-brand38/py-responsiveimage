'''
MIT License
Copyright (c) 2023 Pascal Brand

Extends argparse
'''

import argparse


def _check_arg_errors(argsparsed: argparse.Namespace) -> argparse.Namespace:
  # update argsparsed, and check for errors
  if (argsparsed.size is not None) and (argsparsed.height is not None):
    raise RuntimeError("--size and --height cannot be both set")

  if (argsparsed.size is None) and (argsparsed.height is None):
    argsparsed.size = '1920'

  if (argsparsed.size is not None):
    transform = argsparsed.size.split(',')
  elif (argsparsed.height is not None):
    transform = argsparsed.height.split(',')
  else:
    raise RuntimeError("Developer issue")

  if argsparsed.add_name is None:
    if len(transform) == 1:
      argsparsed.add_name = ''
    else:
      argsparsed.add_name = '-' + ',-'.join(transform)
  else:
    # check length of add_name is same as length of transform
    if argsparsed.add_name.count(',') != len(transform)-1:
      raise RuntimeError("--size (or --height) and --add-name must have the same number of elements")

  if argsparsed.crop is not None:
    values = argsparsed.crop.split(',')
    if len(values) != 4:
      raise RuntimeError("--crop must be equal to a,b,c,d (4 values)")
    for index, _ in enumerate(values):
      values[index] = int(values[index])
    argsparsed.crop = values

  values = argsparsed.format.split(',')
  for index, _ in enumerate(values):
    values[index] = values[index].lower()
  argsparsed.format = values

  return argsparsed

class argsResponsiveImage():
  '''
  extends argparse
  '''
  def __init__(self, argsparsed: argparse.Namespace, nb: int) -> None:
    argsparsed = _check_arg_errors(argsparsed)

    self.args = argsparsed
    self.nb = nb
    self.parameters = {   # TODO: add a commandline option to update it dynamically
      'jpg': {
        'quality': 80,
        'progressive': True,
        'subsampling': '4:2:0',
        },
      'webp': {
        'quality': 80,
      }
    }

  def add(self, nb) -> None:
    '''
    increment the number of processed images
    '''
    self.nb = self.nb + nb

  def print(self, filename: str, processed: bool, nb: int) -> None:
    '''
    verbose the number of processed images
    '''
    if (processed):
      print('  + ' + str(nb) + ' ' + filename)
    else:
      print('  - ' + str(nb) + ' ' + filename)
