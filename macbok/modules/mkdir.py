from __future__ import print_function
from __future__ import unicode_literals

import errno
import os
import stat

from macbok.common import task
from macbok.modules import script


class MkDir(task.Task):

  def __init__(self, target, sudo=False):
    """Creates an empty directory.

    Args:
      target: The path of the directory
      sudo: Whether sudo is required
    """
    self.target = target
    self.sudo = sudo

  def __repr__(self):
    arguments = [self.target]
    if self.sudo:
      arguments.append('sudo=%r' % self.sudo)
    return 'MkDir(%s)' % (', '.join(arguments))

  def OnlyIf(self):
    try:
      s = os.lstat(self.target)
    except OSError as e:
      if e.args[0] == errno.ENOENT:
        return True
      else:
        raise
    else:
      if not stat.S_ISDIR(s.st_mode):
        raise OSError('Target %r exists but is not a directory.' % self.target)
    return False

  def Run(self):
    if self.sudo:
      yield script.Script(['sudo', 'mkdir', '-p', self.target])
    else:
      os.mkdir(self.target)
