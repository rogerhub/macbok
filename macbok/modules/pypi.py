from macbok.common import task
from macbok.common import util
from macbok.modules import homebrew
from macbok.modules import script


class Pypi(task.Task):
  """Installs Python 3 packages from PyPI to the local user home directory."""

  def __init__(self, package=None, version=None):
    self.package = package
    self.version = version

  def __repr__(self):
    arguments = []
    if self.package:
      arguments.append(repr(self.package))
    if self.version:
      arguments.append('version=%r' % self.version)
    return 'Pypi(%s)' % (', '.join(arguments))

  def _AlreadyInstalled(self):
    return bool(util.Which('pip3'))

  def _InstalledPackages(self):
    from pip.utils import get_installed_distributions
    return [package.project_name
            for package in get_installed_distributions(user_only=True)]

  def OnlyIf(self):
    with self.TaskLock():
      if not self._AlreadyInstalled():
        return True
      if self.package and self.package not in self._InstalledPackages():
        return True

  def Run(self):
    with self.TaskLock():
      if not self._AlreadyInstalled():
        yield homebrew.Homebrew('python3')
      if self.package and self.package not in self._InstalledPackages():
        extra_options = ['--user', '--ignore-installed']
        if self.version:
          target = '%s==%s' % (self.package, self.version)
        else:
          target = self.package
        command = 'pip3 install %s %s' % (' '.join(extra_options),
                                          util.BashQuote(target))
        yield script.Script(command)
