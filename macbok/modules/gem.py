import json
from macbok.common.task import Task
from macbok.common.util import bash_quote
from macbok.modules.script import Script


class Gem(Task):
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
      arguments.append("version=%s" % repr(self.version))
    return "Gem(%s)" % (", ".join(arguments))

  def onlyif(self):
    if self.package:
      with self.task_lock():
        payload = "require 'json'; puts JSON::dump Gem::Specification.map {|g| g.name}"
        installed_packages_bytes = yield Script(
            "ruby -e %s" % bash_quote(payload), _internal=True)
        installed_packages = json.loads(installed_packages_bytes)
        yield self.package not in installed_packages

  def run(self):
    with self.task_lock():
      extra_options = "--user-install"
      if self.version:
        target = "%s==%s" % (self.package, self.version)
      else:
        target = self.package
      command = "gem install %s %s" % (extra_options, bash_quote(target))
      yield Script(command)
