"""
MIT License
Copyright (c) 2025 Pascal Brand

Unit testing utility
"""

import os

def resDir(test: str):
  dir = 'tests/results'
  if not os.path.exists(dir):
    os.makedirs(dir)
  dir = dir + '/' + test
  if not os.path.exists(dir):
    os.makedirs(dir)
  return dir
