import json
from macbok.common import task
from macbok.common import util
from macbok.modules import script


class Gem(task.Task):
  """Installs a ruby gem to the home directory.

  You will need to add ~/.gem/ruby/*/bin to your PATH in order for Gem bundled
  scripts to work.
  """

  def __init__(self, package=None, version=None):
    self.package = package
    self.version = version

  def __repr__(self):
    arguments = []
    if self.package:
      arguments.append(repr(self.package))
    if self.version:
      arguments.append('version=%s' % repr(self.version))
    return 'Gem(%s)' % (', '.join(arguments))

  def OnlyIf(self):
    if not self.package:
      return
    with self.task_lock():
      payload = ('require "json";'
                 'puts JSON::dump Gem::Specification.map {|g| g.name}')
      command = 'ruby -e %s' % util.BashQuote(payload)
      packages_bytes = yield script.Script(command, _internal=True)
      packages = json.loads(packages_bytes)
      yield self.package not in packages

  def Run(self):
    with self.TaskLock():
      extra_options = '--user-install'
      if self.version:
        target = '%s==%s' % (self.package, self.version)
      else:
        target = self.package
      command = 'gem install %s %s' % (extra_options, util.BashQuote(target))
      yield script.Script(command)
