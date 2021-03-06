import errno
import os
import stat

from macbok.common import task


class Link(task.Task):
  def __init__(self, target, path):
    """Creates a symbolic link. Equivalent to `ln -s $target $path`

    Args:
      target: The value of this symbolic link
      path: Where to create the symbolic link on the file system
    """
    self.target = target
    self.path = path

  def __repr__(self):
    return 'Link(%r, %r)' % (self.target, self.path)

  def OnlyIf(self):
    try:
      stat_result = os.lstat(self.path)
      if not stat.S_ISLNK(stat_result.st_mode):
        raise ValueError('%s already exists, but is not a link' % self.path)
      if self.target != os.readlink(self.path):
        return True
    except OSError as e:
      if e.args[0] == errno.ENOENT:
        return True
      else:
        raise

  def Run(self):
    try:
      stat_result = os.lstat(self.path)
      if not stat.S_ISLNK(stat_result.st_mode):
        raise ValueError('%s already exists, but is not a link' % self.path)
      os.unlink(self.path)
    except OSError as e:
      if e.args[0] != errno.ENOENT:
        raise
    os.symlink(self.target, self.path)
