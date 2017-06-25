from macbok.common.task import Task
from macbok.common.util import bash_quote
from macbok.modules.script import Script
from os.path import exists, join


class Gitclone(Task):
  """Clones a git repository."""

  def __init__(self, source, target, recursive=False):
    self.source = source
    self.target = target
    self.recursive = recursive

  def __repr__(self):
    arguments = [repr(self.source), repr(self.target)]
    if self.recursive:
      arguments.append("recursive=%s" % repr(self.recursive))
    return "Gitclone(%s)" % (", ".join(arguments))

  def onlyif(self):
    if not exists(join(self.target, ".git")):
      return True

  def run(self):
    extra_options = ""
    if self.recursive:
      extra_options = "--recursive"
    yield Script("git clone %s -- %s %s" % (extra_options,
                                            bash_quote(self.source),
                                            bash_quote(self.target)))
