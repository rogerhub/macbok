#!/usr/bin/env python3

from __future__ import print_function

import macbok
import sys
from macbok.common.util import get_username
from macbok.modules.chown import Chown
from macbok.modules.defaults import Defaults
from macbok.modules.gem import Gem
from macbok.modules.gitclone import Gitclone
from macbok.modules.homebrew import Homebrew
from macbok.modules.link import Link
from macbok.modules.npm import Npm
from macbok.modules.pypi import Pypi
from os import mkdir
from os.path import exists, expanduser


def main():
    """
    A fully-functional example of a typical user's OS X configuration.

    """
    # Do not create .DS_Store on network shares
    yield Defaults("com.apple.desktopservices", "DSDontWriteNetworkStores", True)

    # Disable autocorrect
    yield Defaults("NSGlobalDomain", "NSAutomaticSpellingCorrectionEnabled", False)

    # Disables keyboard press-and-hold for accented character entry
    yield Defaults("NSGlobalDomain", "ApplePressAndHoldEnabled", False)

    # Expand the Save panel by default
    yield Defaults("NSGlobalDomain", "NSNavPanelExpandedStateForSaveMode", True)

    # Sets the delay before held keys repeat
    yield Defaults("NSGlobalDomain", "InitialKeyRepeat", 15)

    # Sets the repeat rate for held keys
    yield Defaults("NSGlobalDomain", "KeyRepeat", 2)

    # Minimize windows to dock icon
    yield Defaults("com.apple.dock", "minimize-to-application", True)

    # Put the dock on the bottom
    yield Defaults("com.apple.dock", "orientation", "bottom")

    # Change icon size
    yield Defaults("com.apple.dock", "tilesize", 36)

    # Auto-hide the dock
    yield Defaults("com.apple.dock", "autohide", 0)

    # Fast updates for Activity Monitor (every second)
    yield Defaults("com.apple.ActivityMonitor", "UpdatePeriod", 1)

    # Dark interface
    yield Defaults("Apple Global Domain", "AppleInterfaceStyle", "Dark")

    # Finder show all file extensions
    yield Defaults("Apple Global Domain", "AppleShowAllExtensions", 1)

    # Only show scrollbars when scrolling
    yield Defaults("Apple Global Domain", "AppleShowScrollBars", "WhenScrolling")

    # Set ask for password delay to 0
    yield Defaults("com.apple.screensaver", "askForPasswordDelay", 0)

    # Turn off Apple Airplay status bar icon
    yield Defaults("com.apple.airplay", "showInMenuBarIfPresent", 0)

    yield Link("Bok/Configuration", expanduser("~/Configuration"))

    if exists(expanduser("~/Bok/Configuration")):
        # Avoid creating a dead links
        if not exists(expanduser("~/.atom")):
            mkdir(expanduser("~/.atom"))
        for atom_path in ["config.cson", "keymap.cson", "snippets.cson", "styles.less"]:
            yield Link("../Configuration/atom/" + atom_path, expanduser("~/.atom/" + atom_path))
        yield Link("Configuration/bcrc", expanduser("~/.bcrc"))
        yield Link("Configuration/gitconfig", expanduser("~/.gitconfig"))
        yield Link("Configuration/gitignore", expanduser("~/.gitignore"))
        yield Link("Configuration/zshconfig", expanduser("~/.zshconfig"))
        if not exists(expanduser("~/.ssh")):
            mkdir(expanduser("~/.ssh"))
        if not exists(expanduser("~/.ssh/ctl")):
            mkdir(expanduser("~/.ssh/ctl"))
        yield Link("../Configuration/ssh/known_hosts", expanduser("~/.ssh/known_hosts"))
        yield Link("../Configuration/ssh/config", expanduser("~/.ssh/config"))
        yield Link("Configuration/pydistutils.cfg", expanduser("~/.pydistutils.cfg"))

    if exists(expanduser("~/.gradle")):
        yield Link("../Configuration/gradle.properties", expanduser("~/.gradle/gradle.properties"))

    yield Chown("/etc/hosts", get_username(), group="staff")

    # Basic packages
    yield Homebrew(tap="homebrew/core")
    yield Homebrew(tap="caskroom/cask")
    yield Homebrew(tap="homebrew/fuse")
    yield Homebrew(tap="homebrew/x11")
    yield Homebrew(tap="homebrew/science")
    yield Homebrew("gcc", force_bottle=True)
    yield Homebrew("awscli")
    yield Homebrew("fswatch", force_bottle=True)
    yield Homebrew("go", force_bottle=True)
    yield Homebrew("ctags", force_bottle=True)
    yield Homebrew("the_silver_searcher", force_bottle=True)
    yield Homebrew("ant", force_bottle=True)
    yield Homebrew("wget", force_bottle=True)
    yield Homebrew("pstree", force_bottle=True)
    yield Homebrew("duplicity", force_bottle=True)
    yield Homebrew("mcrypt", force_bottle=True)
    yield Homebrew("iperf")
    yield Homebrew("mtr", force_bottle=True)
    yield Homebrew("unrar", force_bottle=True)
    yield Homebrew("htop-osx", force_bottle=True)
    yield Homebrew("wakeonlan")
    yield Homebrew("openssl", force_bottle=True)
    yield Homebrew("imagemagick", force_bottle=True)
    yield Homebrew("gettext", force_bottle=True)
    yield Homebrew("python", force_bottle=True)
    yield Homebrew("python3", force_bottle=True)
    yield Homebrew("node", force_bottle=True)
    yield Homebrew("hping")
    yield Homebrew("ffmpeg", force_bottle=True)
    yield Homebrew("clang-format", force_bottle=True)
    yield Homebrew("git", force_bottle=True)
    yield Homebrew("webp", force_bottle=True)
    yield Homebrew("nmap", force_bottle=True)
    yield Homebrew("nasm", force_bottle=True)
    yield Homebrew("doctl", force_bottle=True)
    yield Homebrew("source-highlight", force_bottle=True)
    yield Homebrew("lftp", force_bottle=True)
    yield Homebrew("arping", force_bottle=True)

    # Fuse-related packages
    yield Homebrew(cask_package="osxfuse")
    yield Homebrew(cask_package="sshfs")
    yield Homebrew("fuse-zip", force_bottle=True)

    # Java-related packages
    yield Homebrew(cask_package="java")
    yield Homebrew("maven", force_bottle=True)
    yield Homebrew("scala", force_bottle=True)
    yield Homebrew("gradle")

    # X11-related packages
    # yield Homebrew(cask_package="xquartz")
    # yield Homebrew("rdesktop", force_bottle=True)

    # Cask packages
    yield Homebrew(cask_package="google-chrome")
    yield Homebrew(cask_package="gnucash")
    # yield Homebrew(cask_package="google-hangouts")
    yield Homebrew(cask_package="vlc")
    yield Homebrew(cask_package="calibre")
    yield Homebrew(cask_package="caffeine")
    yield Homebrew(cask_package="vmware-fusion")
    yield Homebrew(cask_package="dropbox")
    yield Homebrew(cask_package="spotify")
    yield Homebrew(cask_package="logitech-options")
    yield Homebrew(cask_package="google-cloud-sdk")
    yield Homebrew(cask_package="atom")
    yield Homebrew(cask_package="wireshark")
    yield Homebrew(cask_package="1password")
    yield Homebrew(cask_package="handbrake")

    if sys.executable != "/usr/local/opt/python3/bin/python3.5":
        print("Please restart your shell and run this script again using homebrew's python")
        sys.exit(0)

    yield Pypi("boto")
    yield Pypi("flake8")
    yield Pypi("ipdb")
    yield Pypi("ipython")
    yield Pypi("line-profiler")
    yield Pypi("matplotlib", version="1.4.3")
    yield Pypi("numpy")
    yield Pypi("Pillow")
    yield Pypi("pytest")
    yield Pypi("requests")
    yield Pypi("scipy")
    yield Pypi("scikit-image")
    yield Pypi("scikit-learn")
    yield Pypi("unittest2")
    yield Pypi("virtualenv")
    yield Pypi("websocket-client")
    yield Pypi("pyOpenSSL")
    yield Pypi("autopep8")
    yield Pypi("python-geoip")
    yield Pypi("python-geoip-geolite2")
    yield Pypi("Cython")
    yield Pypi("pycrypto")
    yield Pypi("PyYAML")
    yield Pypi("six")
    yield Pypi("nose")

    yield Gem("sass")
    yield Gem("jekyll")

    yield Npm("uglify-js")
    yield Npm("coffee-script")

    # Mactex is hosted on some remote European web server.
    # It takes forever to download (1-2 hours) regardless of your internet connection, so do it last.
    yield Homebrew(cask_package="mactex")


if __name__ == "__main__":
    macbok.execute(main)
