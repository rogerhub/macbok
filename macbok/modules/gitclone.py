from os import path

from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Gitclone(task.Task):
  """Clones a git repository."""

  def __init__(self, source, target, recursive=False):
    self.source = source
    self.target = target
    self.recursive = recursive

  def __repr__(self):
    arguments = [repr(self.source), repr(self.target)]
    if self.recursive:
      arguments.append('recursive=%r' % self.recursive)
    return 'Gitclone(%s)' % (', '.join(arguments))

  def OnlyIf(self):
    if not path.exists(path.join(self.target, '.git')):
      return True

  def Run(self):
    extra_options = []
    if self.recursive:
      extra_options.append('--recursive')
    yield Script('git clone %s -- %s %s' % (' '.join(extra_options),
                                            util.BashQuote(self.source),
                                            util.BashQuote(self.target)))
