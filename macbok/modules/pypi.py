from macbok.common.task import Task
from macbok.common.util import bash_quote, which
from macbok.modules.script import Script


class Pypi(Task):
    """
    Installs Python packages from PyPI to the local user home directory, via pip.
    System packages with the same name will be shadowed. Usage example:

        yield Pypi("numpy")

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
        return "Pypi(%s)" % (", ".join(arguments))

    def _already_installed(self):
        return bool(which("pip"))

    def _installed_packages(self):
        from pip.utils import get_installed_distributions
        return [package.project_name for package in get_installed_distributions(user_only=True)]

    def onlyif(self):
        with self.task_lock():
            if not self._already_installed():
                return True
            if self.package and self.package not in self._installed_packages():
                return True

    def run(self):
        with self.task_lock():
            if not self._already_installed():
                yield Script("sudo easy_install pip")
            if self.package and self.package not in self._installed_packages():
                extra_options = "--user --ignore-installed"
                if self.version:
                    target = "%s==%s" % (self.package, self.version)
                else:
                    target = self.package
                command = "pip install %s %s" % (extra_options, bash_quote(target))
                yield Script(command)
