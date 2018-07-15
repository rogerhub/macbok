from __future__ import unicode_literals

import logging

from macbok.common import task
from macbok.common import util
from macbok.modules import chown
from macbok.modules import script


class Sysctl(task.Task):

  def __init__(self, key, value):
    """Sets a sysctl value."""
    self.key = key
    self.value = value

  def __repr__(self):
    return 'Sysctl(%r, %r)' % (self.key, self.value)

  def OnlyIf(self):
    try:
      with open('/private/etc/sysctl.conf', 'r') as f:
        return '%s=%s\n' % (self.key, self.value) not in f.read()
    except (IOError, OSError) as e:
      return True

  def Run(self):
    yield script.Script(
        'echo %s=%s | sudo tee -a /private/etc/sysctl.conf' %
        (util.BashQuote(self.key), util.BashQuote(self.value)))
