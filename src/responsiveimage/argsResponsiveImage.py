'''
MIT License
Copyright (c) 2023 Pascal Brand

TODO
'''

class argsResponsiveImage():
  '''
  extends argparse
  '''
  def __init__(self, argsparsed, nb:int|None=None):
    self.args = argsparsed
    self.nb = nb
    self.parameters = {
      'jpg': {
        'quality': 80,
        'progressive': True,
        'subsampling': '4:2:0',
        },
      'webp': {
        'quality': 80,
      }
    }

  def inc(self):
    '''
    increment the number of processed images
    '''
    if self.nb is not None:
      self.nb = self.nb + 1

  def print(self, filename: str, processed: bool):
    '''
    verbose the number of processed images
    '''
    if self.nb is not None:
      if (processed):
        print('  + ' + str(self.nb) + ' ' + filename)
      else:
        print('  - ' + str(self.nb) + ' ' + filename)
