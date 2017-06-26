from __future__ import unicode_literals

from os import path

from backports import plistlib
from macbok.common import task


def _Resolve(plist, key):
  p = plist
  for k in key:
    try:
      p = p[k]
    except (KeyError, IndexError):
      raise KeyError('Key %r not in %s' % (k, p))
  return p


class Plist(task.Task):
  def __init__(self, key, value, domain='.GlobalPreferences'):
    if isinstance(key, str):
      key = (key,)
    elif not isinstance(key, tuple):
      raise ValueError('Unrecognized key type: %r' % key)
    if not key:
      raise ValueError('Key must not be empty.')
    self.key = key
    self.value = value
    self.domain = domain

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
    return path.expanduser('~/Library/Preferences/%s.plist' % self.domain)

  def _ReadPlist(self):
    with open(self._PlistPath(), 'rb') as plist_file:
      return plistlib.load(plist_file)

  def OnlyIf(self):
    with self.TaskLock():
      plist = self._ReadPlist()
      p = _Resolve(plist, self.key[:-1])
      return p.get(self.key[-1]) != self.value

  def Run(self):
    with self.TaskLock():
      plist = self._ReadPlist()
      p = _Resolve(plist, self.key[:-1])
      p[self.key[-1]] = self.value
      with open(self._PlistPath(), 'wb') as plist_file:
        plistlib.dump(plist, plist_file, fmt=plistlib.FMT_BINARY)
