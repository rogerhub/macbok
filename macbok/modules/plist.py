from __future__ import unicode_literals

from os import path
import subprocess

from backports import plistlib
from macbok.common import task
from macbok.common import util
from macbok.modules import chown


def _Resolve(plist, key):
  p = plist
  for k in key:
    try:
      p = p[k]
    except (KeyError, IndexError):
      raise KeyError('Key %r not in %s' % (k, p))
  return p


class Plist(task.Task):
  def __init__(self, key, value, domain='.GlobalPreferences', sudo=False):
    if isinstance(key, type('')):
      key = (key,)
    elif not isinstance(key, tuple):
      raise ValueError('Unrecognized key type: %r' % key)
    if not key:
      raise ValueError('Key must not be empty.')
    self.key = key
    self.value = value
    self.domain = domain
    self.sudo = sudo

  def __repr__(self):
    arguments = []
    if len(self.key) == 1:
      arguments.append(repr(self.key[0]))
    else:
      arguments.append(repr(self.key))
    arguments.append(repr(self.value))
    if self.domain != '.GlobalPreferences':
      arguments.append('domain=%r' % self.domain)
    return 'Plist(%s)' % ', '.join(arguments)

  def _PlistPath(self):
    if self.sudo:
      return '/Library/Preferences/%s.plist' % self.domain
    else:
      return path.expanduser('~/Library/Preferences/%s.plist' % self.domain)

  def _ReadPlist(self):
    with open(self._PlistPath(), 'rb') as plist_file:
      return plistlib.load(plist_file)

  def OnlyIf(self):
    with self.TaskLock():
      try:
        plist = self._ReadPlist()
      except IOError as e:
        print('Error reading plist: %s' % e)
        return False
      p = _Resolve(plist, self.key[:-1])
      return p.get(self.key[-1]) != self.value

  def Run(self):
    with self.TaskLock():
      plist = self._ReadPlist()
      p = _Resolve(plist, self.key[:-1])
      if self.value is None:
        del p[self.key[-1]]
      else:
        if self.key[-1] not in p:
          raise ValueError('Key %s not in %s', self.key[-1], p.keys())
        p[self.key[-1]] = self.value
      if self.sudo:
        # TODO: This is hacky, but it works.
        yield chown.Chown(self._PlistPath(), user=util.Username())
      with open(self._PlistPath(), 'wb') as plist_file:
        plistlib.dump(plist, plist_file, fmt=plistlib.FMT_BINARY)
      if self.sudo:
        yield chown.Chown(self._PlistPath(), user='root')
