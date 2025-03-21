"""
MIT License
Copyright (c) 2025 Pascal Brand

Unit testing utility
"""

import os

def resDir(test: str):
  """
  get results dir, for artifacts, and create it if necessary
  - extension are the same
  - size are the same, up to 25%
  """

  res = 'tests/results'
  if not os.path.exists(res):
    os.makedirs(res)
  res = res + '/' + test
  if not os.path.exists(res):
    os.makedirs(res)
  return res
