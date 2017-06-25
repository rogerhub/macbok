import os
from os import path

from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Npm(task.Task):
  """Installs npm packages globally."""

  installation_root = '/usr/local'

  def __init__(self, package=None, version=None):
    self.package = package
    self.version = version

  def __repr__(self):
    arguments = []
    if self.package:
      arguments.append(repr(self.package))
    if self.version:
      arguments.append('version=%r' % self.version)
    return 'Npm(%s)' % (', '.join(arguments))

  def _InstalledPackages(self):
    packages_directory = path.join(self.installation_root, 'lib',
                                   'node_modules')
    if not path.exists(packages_directory):
      return []
    else:
      return os.listdir(packages_directory)

  def OnlyIf(self):
    with self.TaskLock():
      if self.package and self.package not in self._InstalledPackages():
        return True

  def Run(self):
    with self.TaskLock():
      if self.package and self.package not in self._InstalledPackages():
        extra_options = '--global'
        if self.version:
          target = '%s@%s' % (self.package, self.version)
        else:
          target = self.package
        command = 'npm install %s %s' % (extra_options, util.BashQuote(target))
        yield script.Script(command)
