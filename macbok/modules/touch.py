import os
from os import path

from macbok.common import task

class Touch(task.Task):
  def __init__(self, target):
    """Creates an empty file.

    Args:
      target: The path of the file
    """
    self.target = target

  def __repr__(self):
    return 'Touch(%r)' % self.target

  def OnlyIf(self):
    return not path.exists(self.target)

  def Run(self):
    open(self.target, 'a').close()
