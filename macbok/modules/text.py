from __future__ import print_function
from __future__ import unicode_literals

import errno
import os
import stat

from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Text(task.Task):

  def __init__(self, target, content, sudo=False):
    self.target = target
    self.content = content
    self.sudo = sudo

  def __repr__(self):
    arguments = [self.target, self.content]
    if self.sudo:
      arguments.append('sudo=%r' % self.sudo)
    return 'Text(%s)' % (', '.join(arguments))

  def OnlyIf(self):
    return not os.path.exists(self.target)

  def Run(self):
    if self.sudo:
      yield script.Script('echo %s | sudo tee %s >/dev/null' % (
          util.BashQuote(self.content), self.target))
    else:
      with open(self.target, 'w') as f:
        f.write(self.content)
