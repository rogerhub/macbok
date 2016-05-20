import re
from glob import glob
from macbok.common.task import Task
from macbok.common.util import bash_quote, get_username
from macbok.modules.chown import Chown
from macbok.modules.gitclone import Gitclone
from macbok.modules.script import Script
from os import listdir
from os.path import exists, join


class Homebrew(Task):
    installation_root = "/usr/local"
    cask_installation_root = "/opt/homebrew-cask"

    def __init__(self, package=None, cask_package=None, tap=None, force_bottle=False):
        """
        Installs a homebrew package, homebrew cask package, or homebrew tap.

        """
        self.package = package
        self.tap = tap
        self.cask_package = cask_package
        self.force_bottle = force_bottle

    def __repr__(self):
        arguments = []
        if self.package:
            arguments.append(repr(self.package))
        if self.cask_package:
            arguments.append("cask_package=%s" % repr(self.cask_package))
        if self.tap:
            arguments.append("tap=%s" % repr(self.tap))
        if self.force_bottle:
            arguments.append("force_bottle=%s" % repr(self.force_bottle))
        return "Homebrew(%s)" % (", ".join(arguments))

    def _already_installed(self):
        return exists(join(self.installation_root, "bin/brew"))

    def _installed_packages(self):
        cellar_directory = join(self.installation_root, "Cellar")
        if not exists(cellar_directory):
            return []
        else:
            return listdir(cellar_directory)

    def _taps(self):
        tap_paths = glob(join(self.installation_root, "Library", "Taps", "*", "homebrew-*"))
        tap_path_matcher = re.compile(".*Taps/(?P<org>.*)/homebrew-(?P<tap>.*)$")
        taps = []
        for tap_path in tap_paths:
            tap_path_match = tap_path_matcher.match(tap_path)
            if tap_path_match:
                taps.append("%s/%s" % (tap_path_match.group("org"), tap_path_match.group("tap")))
        return taps

    def _cask_installed_packages(self):
        caskroom_directory = join(self.cask_installation_root, "Caskroom")
        if not exists(caskroom_directory):
            return []
        else:
            return listdir(caskroom_directory)

    def onlyif(self):
        with self.task_lock():
            if not self._already_installed:
                return True
            if self.package and self.package not in self._installed_packages():
                return True
            if self.cask_package:
                if self.cask_package not in self._cask_installed_packages():
                    return True
            if self.tap and self.tap not in self._taps():
                return True

    def run(self):
        with self.task_lock():
            if not self._already_installed():
                yield Chown(self.installation_root, get_username())
                yield Gitclone("https://github.com/Homebrew/homebrew.git", self.installation_root)
            if self.package and self.package not in self._installed_packages():
                extra_options = ""
                if self.force_bottle:
                    extra_options = "--force-bottle"
                yield Script("brew install %s %s" % (extra_options, bash_quote(self.package)))
            if self.cask_package:
                if self.cask_package not in self._cask_installed_packages():
                    yield Script("brew cask install %s" % bash_quote(self.cask_package))
            if self.tap and self.tap not in self._taps():
                yield Script("brew tap %s" % bash_quote(self.tap))
