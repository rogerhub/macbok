from macbok.common.task import Task
from macbok.common.util import bash_quote
from macbok.modules.script import Script
from os import listdir
from os.path import exists, join


class Npm(Task):
    """
    Installs npm packages globally.

    """

    installation_root = "/usr/local"

    def __init__(self, package=None, version=None):
        self.package = package
        self.version = version

    def __repr__(self):
        arguments = []
        if self.package:
            arguments.append(repr(self.package))
        if self.version:
            arguments.append("version=%s" % repr(self.version))
        return "Npm(%s)" % (", ".join(arguments))

    def _installed_packages(self):
        packages_directory = join(self.installation_root, "lib", "node_modules")
        if not exists(packages_directory):
            return []
        else:
            return listdir(packages_directory)

    def onlyif(self):
        with self.task_lock():
            if self.package and self.package not in self._installed_packages():
                return True

    def run(self):
        with self.task_lock():
            if self.package and self.package not in self._installed_packages():
                extra_options = "--global"
                if self.version:
                    target = "%s@%s" % (self.package, self.version)
                else:
                    target = self.package
                command = "npm install %s %s" % (extra_options, bash_quote(target))
                yield Script(command)

