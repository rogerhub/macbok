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
from macbok.modules.pmset import Pmset
from macbok.modules.pypi import Pypi
from macbok.modules.touch import Touch
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
    # yield Defaults("NSGlobalDomain", "InitialKeyRepeat", 15)

    # Sets the repeat rate for held keys
    # yield Defaults("NSGlobalDomain", "KeyRepeat", 2)

    # Minimize windows to dock icon
    yield Defaults("com.apple.dock", "minimize-to-application", True)

    # Put the dock on the bottom
    yield Defaults("com.apple.dock", "orientation", "bottom")

    # Change icon size
    yield Defaults("com.apple.dock", "tilesize", 52)

    # Auto-hide the dock
    yield Defaults("com.apple.dock", "autohide", 1)

    # Fast updates for Activity Monitor (every second)
    yield Defaults("com.apple.ActivityMonitor", "UpdatePeriod", 1)

    # Dark interface
    # yield Defaults("Apple Global Domain", "AppleInterfaceStyle", "Dark")

    # Finder show all file extensions
    yield Defaults("Apple Global Domain", "AppleShowAllExtensions", 1)

    # Only show scrollbars when scrolling
    yield Defaults("Apple Global Domain", "AppleShowScrollBars", "WhenScrolling")

    # Set ask for password delay to 0
    yield Defaults("com.apple.screensaver", "askForPasswordDelay", 0)

    # Turn off Apple Airplay status bar icon
    yield Defaults("com.apple.airplay", "showInMenuBarIfPresent", 0)

    # Turn off Finder opening when Transmit mounts.
    if exists(expanduser("~/Library/Preferences/com.panic.Transmit.plist")):
        yield Defaults("com.panic.transmit", "OpenMountedFinderWindow", False)

    yield Link("Library/Application Support/MobileSync", expanduser("~/MobileSync"))

    if exists(expanduser("~/C8")):
        # Avoid creating a dead links
        if not exists(expanduser("~/.atom")):
            mkdir(expanduser("~/.atom"))
        for atom_path in ["config.cson", "init.coffee", "keymap.cson", "snippets.cson", "styles.less"]:
            yield Link("../C8/atom/" + atom_path, expanduser("~/.atom/" + atom_path))
        yield Link("C8/.bcrc", expanduser("~/.bcrc"))
        yield Link("C8/.gitconfig", expanduser("~/.gitconfig"))
        yield Link("C8/.gitignore", expanduser("~/.gitignore"))
        yield Link("C8/.bash_aliases", expanduser("~/.bash_aliases"))
        yield Link("C8/.bash_profile", expanduser("~/.bash_profile"))
        if not exists(expanduser("~/.ssh")):
            mkdir(expanduser("~/.ssh"))
        yield Link("../C8/.ssh/known_hosts", expanduser("~/.ssh/known_hosts"))
        yield Link("../C8/.ssh/config", expanduser("~/.ssh/config"))
        if not exists(expanduser("~/.ssh/ctl")):
            mkdir(expanduser("~/.ssh/ctl"))

    yield Touch(expanduser("~/.bash_sessions_disable"))

    # Chrome doesn't respect /etc/hosts if not owned by root (?)
    # yield Chown("/etc/hosts", get_username(), group="staff")

    # Basic packages
    yield Homebrew(tap="homebrew/core")
    yield Homebrew(tap="caskroom/cask")
    yield Homebrew(tap="caskroom/drivers")
    yield Homebrew(tap="caskroom/versions")
    yield Homebrew(tap="homebrew/fuse")
    yield Homebrew(tap="homebrew/x11")
    yield Homebrew(tap="homebrew/science")
    yield Homebrew(tap="rogerhub/sman")
    yield Homebrew(tap="rogerhub/transmit-disk")
    yield Homebrew("pstree", force_bottle=True)
    yield Homebrew("duplicity", force_bottle=True)
    yield Homebrew("mcrypt", force_bottle=True)
    # yield Homebrew("iperf")
    yield Homebrew("mtr", force_bottle=True)
    yield Homebrew("unrar", force_bottle=True)
    yield Homebrew("wakeonlan")
    yield Homebrew("openssl", force_bottle=True)
    # yield Homebrew("imagemagick", force_bottle=True)
    # yield Homebrew("gettext", force_bottle=True)
    yield Homebrew("python", force_bottle=True)
    yield Homebrew("python3", force_bottle=True)
    # yield Homebrew("hping")
    # yield Homebrew("ffmpeg", force_bottle=True)
    yield Homebrew("git", force_bottle=True)
    # yield Homebrew("webp", force_bottle=True)
    yield Homebrew("nmap", force_bottle=True)
    # yield Homebrew("nasm", force_bottle=True)
    yield Homebrew("source-highlight", force_bottle=True)
    # yield Homebrew("lftp", force_bottle=True)
    yield Homebrew("arping", force_bottle=True)
    yield Homebrew("socat", force_bottle=True)
    yield Homebrew("colordiff", force_bottle=True)

    # Fuse-related packages
    yield Homebrew(cask_package="osxfuse")
    yield Homebrew("sshfs")
    yield Homebrew("fuse-zip", force_bottle=True)

    # Cask packages
    yield Homebrew(cask_package="google-chrome")
    yield Homebrew(cask_package="gnucash")
    yield Homebrew(cask_package="vlc")
    yield Homebrew(cask_package="calibre")
    yield Homebrew(cask_package="vmware-fusion")
    yield Homebrew(cask_package="logitech-options")
    yield Homebrew(cask_package="atom")
    # yield Homebrew(cask_package="wireshark")
    yield Homebrew(cask_package="1password")
    yield Homebrew(cask_package="handbrake")
    yield Homebrew(cask_package="sman")
    # yield Homebrew(cask_package="unetbootin")
    yield Homebrew(cask_package="transmit")
    yield Homebrew(cask_package="transmit-disk")

    # Mactex is hosted on some remote European web server.
    # It takes forever to download (1-2 hours) regardless of your internet connection, so do it last.
    # yield Homebrew(cask_package="mactex")


if __name__ == "__main__":
    macbok.execute(main)
