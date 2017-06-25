import os
from macbok.common.task import Task
from os import path

class Touch(Task):
  def __init__(self, target):
    """Creates an empty file

    Args:
      target: The path of the file
    """
    self.target = target

  def __repr__(self):
    return "Touch(%r)" % self.target

  def onlyif(self):
    return not path.exists(self.target)

  def run(self):
    open(self.target, 'a').close()
