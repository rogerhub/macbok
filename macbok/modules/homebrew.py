from __future__ import print_function
from __future__ import unicode_literals

import re
import glob
import os
from os import path

from macbok.common import task
from macbok.common import util
from macbok.modules import chown
from macbok.modules import link
from macbok.modules import gitclone
from macbok.modules import mkdir
from macbok.modules import script


class Homebrew(task.Task):
  """Installs a homebrew package, homebrew cask package, or homebrew tap."""

  installation_root = '/usr/local'
  repository_root = '/usr/local/Homebrew'
  subdirs = [
      'Caskroom', 'Cellar', 'Frameworks', 'Homebrew', 'bin', 'etc',
      'include', 'lib', 'libexec', 'opt', 'sbin', 'share', 'var']

  def __init__(self, package=None, cask_package=None, tap=None,
               force_bottle=False):
    self.package = package
    self.tap = tap
    self.cask_package = cask_package
    self.force_bottle = force_bottle

  def __repr__(self):
    arguments = []
    if self.package:
      arguments.append(repr(self.package))
    if self.cask_package:
      arguments.append('cask_package=%r' % self.cask_package)
    if self.tap:
      arguments.append('tap=%r' % self.tap)
    if self.force_bottle:
      arguments.append('force_bottle=%r' % self.force_bottle)
    return 'Homebrew(%s)' % (', '.join(arguments))

  def _AlreadyInstalled(self):
    return path.exists(path.join(self.installation_root, 'bin/brew'))

  def _InstalledPackages(self):
    cellar_directory = path.join(self.installation_root, 'Cellar')
    if not path.exists(cellar_directory):
      return []
    else:
      return os.listdir(cellar_directory)

  def _Taps(self):
    tap_paths = (glob.glob(path.join(self.repository_root,
                                     'Library', 'Taps', '*', 'homebrew-*')) +
                 glob.glob(path.join(self.installation_root, 'Library', 'Taps',
                                      '*', 'homebrew-*')))
    tap_path_matcher = re.compile(r'.*Taps/(?P<org>.*)/homebrew-(?P<tap>.*)$')
    taps = []
    for tap_path in tap_paths:
      tap_path_match = tap_path_matcher.match(tap_path)
      if tap_path_match:
        taps.append('%s/%s' % (tap_path_match.group('org'),
                               tap_path_match.group('tap')))
    return taps

  def _CaskInstalledPackages(self):
    caskroom_directory = path.join(self.installation_root, 'Caskroom')
    if not path.exists(caskroom_directory):
      return []
    else:
      return os.listdir(caskroom_directory)

  def OnlyIf(self):
    with self.TaskLock():
      if not self._AlreadyInstalled():
        return True
      if self.package and self.package not in self._InstalledPackages():
        return True
      if self.cask_package:
        if self.cask_package not in self._CaskInstalledPackages():
            return True
      if self.tap and self.tap not in self._Taps():
        return True
      return False

  def Run(self):
    with self.TaskLock():
      for d in self.subdirs:
        d = os.path.join(self.installation_root, d)
        yield mkdir.MkDir(d, sudo=True)
        yield chown.Chown(d, util.Username())
      yield gitclone.Gitclone('https://github.com/Homebrew/brew.git',
                              self.repository_root)
      yield link.Link(
          os.path.join(self.repository_root, 'bin', 'brew'),
          os.path.join(self.installation_root, 'bin', 'brew'))

      if self.package and self.package not in self._InstalledPackages():
        extra_options = []
        if self.force_bottle:
          extra_options.append('--force-bottle')
        yield script.Script('brew install %s %s' %
                            (' '.join(extra_options),
                             util.BashQuote(self.package)))
      if self.cask_package:
        if self.cask_package not in self._CaskInstalledPackages():
          yield script.Script('brew cask install %s' %
                              util.BashQuote(self.cask_package))
      if self.tap and self.tap not in self._Taps():
        yield script.Script('brew tap %s' % util.BashQuote(self.tap))
